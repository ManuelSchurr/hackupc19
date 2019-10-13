import requests
import json
import time
from retrieve_nearest_airports import (
    getCoordinates,
    get_coordinates_skyscanner,
    get_nearest_airports,
)


API_KEY = "skyscanner-hackupc2019"
API_URL = "https://www.skyscanner.net/g/chiron/api/v1/"


HEADERS = {
    "user-agent": "HackUPC19",
    "Accept": "application/json",
    "api-key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded",
}

iata_file = open("iatacodes.txt", "r")
iata_codes = iata_file.read().split(",")

# Contains default testing parameters, can - and should - be overwritten
# def browse_quotes(
#     country="DE",
#     currency="EUR",
#     locale="DE",
#     origin_place="FRA",
#     destination_place="TXL",
#     outbound_partial_date="2019-11-11",
#     inbound_partial_date="2019-11-12",
# ):

#     req_url = f"{API_URL}/flights/browse/browsequotes/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
#     response = requests.get(req_url, headers=HEADERS)

#     with open("quotes.json", "w") as outfile:
#         json.dump(response.json(), outfile)


# def browse_routes(
#     country="DE",
#     currency="EUR",
#     locale="DE",
#     origin_place="FRA",
#     destination_place="TXL",
#     outbound_partial_date="2019-11-11",
#     inbound_partial_date="2019-11-12",
# ):
#     req_url = f"{API_URL}/flights/browse/browseroutes/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
#     response = requests.get(req_url, headers=HEADERS)

#     with open("routes.json", "w") as outfile:
#         json.dump(response.json(), outfile)


# def browse_dates(
#     country="DE",
#     currency="EUR",
#     locale="DE",
#     origin_place="FRA",
#     destination_place="TXL",
#     outbound_partial_date="2019-11-11",
#     inbound_partial_date="2019-11-12",
# ):

#     req_url = f"{API_URL}/flights/browse/browsedates/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
#     response = requests.get(req_url, headers=HEADERS)

#     with open("dates.json", "w") as outfile:
#         json.dump(response.json(), outfile)


# def browse_dates_grid(
#     country="DE",
#     currency="EUR",
#     locale="DE",
#     origin_place="FRA",
#     destination_place="TXL",
#     outbound_partial_date="2019-11-11",
#     inbound_partial_date="2019-11-12",
# ):

#     req_url = f"{API_URL}/flights/browse/browsegrid/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
#     response = requests.get(req_url, headers=HEADERS)

#     with open("dates_grid.json", "w") as outfile:
#         json.dump(response.json(), outfile)


# browse_quotes()
# browse_routes()
# browse_dates()
# browse_dates_grid()


def initiate_session(json_params):
    # Start session
    post_url = f"{API_URL}flights/search/pricing/v1.0/"

    response = requests.post(post_url, json=json_params, headers=HEADERS)
    try:
        session_id = response.json()["session_id"]
        print(f"Initiate Session: HTTP {response.status_code}")

        return session_id
    except:
        print("skip dis crap")


def get_airport_id(places, airport_code):
    return next(place for place in places if place["Code"] == airport_code)["Id"]


def get_live_prices(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="TXL",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
    cabin_class="Economy",
    location_schema="iata",
    adults=1,
):
    json_params = {
        "country": country,
        "currency": currency,
        "locale": locale,
        "originPlace": origin_place,
        "destinationPlace": destination_place,
        "outboundDate": outbound_partial_date,
        "inboundDate": inbound_partial_date,
        "cabinClass": cabin_class,
        "locationSchema": location_schema,
        "adults": adults,
    }

    # Initiate the session and get the session id
    session_id = initiate_session(json_params)

    status = "UpdatesPending"

    while status == "UpdatesPending":
        # Poll the result
        req_url = f"{API_URL}flights/search/pricing/v1.0/?session_id={session_id}"
        response = requests.get(req_url, headers=HEADERS)

        status = response.json()["Status"]

        print(f"Get Live Prices: HTTP {response.status_code}")
        print(f"Status:{status}")

        time.sleep(1)

    itineraries = response.json()["Itineraries"]
    # legs = response.json()["Legs"]
    # segments = response.json()["Segments"]
    # places = response.json()["Places"]

    # txl_id = get_airport_id(places, "TXL")
    # fra_id = get_airport_id(places, "FRA")

    sorted_response = dict(response.json())
    sorted_response["Itineraries"] = sorted(
        itineraries, key=lambda x: x["PricingOptions"][0]["Price"]
    )

    # with open("raw_dump.json", "w") as outfile:
    #     json.dump(response.json(), outfile)
    # with open("sorted.json", "w") as outfile:
    #     json.dump(sorted_response, outfile)

    return sorted_response


# get_live_prices()


def find_flight_routes(start_airports, destination_airports, start_date, end_date):
    routes = []

    print(f"all start_airports: {start_airports}")
    print(f"all destination_airports: {destination_airports}")

    for start_airport in start_airports:
        for destination_airport in destination_airports:
            print(
                f"Finding best connection. Currently checking: {start_airport} -> {destination_airport}"
            )
            try:
                sorted_response = get_live_prices(
                    origin_place=start_airport,
                    destination_place=destination_airport,
                    outbound_partial_date=start_date,
                    inbound_partial_date=end_date,
                )

                # Extract itinerary
                itinerary = sorted_response["Itineraries"][0]
                itinerary["PricingOptions"] = itinerary["PricingOptions"][0]

                # Extract legs
                legs = [
                    next(
                        leg
                        for leg in sorted_response["Legs"]
                        if leg["Id"] == itinerary["OutboundLegId"]
                    ),
                    next(
                        leg
                        for leg in sorted_response["Legs"]
                        if leg["Id"] == itinerary["InboundLegId"]
                    ),
                ]
                leg0_segments = []
                leg1_segments = []

                # Extract legs
                for segment_id in legs[0]["SegmentIds"]:
                    leg0_segments.append(
                        next(
                            seg
                            for seg in sorted_response["Segments"]
                            if seg["Id"] == segment_id
                        )
                    )
                for segment_id in legs[1]["SegmentIds"]:
                    leg1_segments.append(
                        next(
                            seg
                            for seg in sorted_response["Segments"]
                            if seg["Id"] == segment_id
                        )
                    )

                segments = [
                    {
                        "OutboundLegSegments": leg0_segments,
                        "InboundLegSegments": leg1_segments,
                    }
                ]

                routes.append(
                    {
                        "Start": start_airport,
                        "Destination": destination_airport,
                        "Itinerary": itinerary,
                        "Legs": legs,
                        "Segments": segments,
                    }
                )
            except Exception as e:
                print("oops")
                print(f"[!] Exception: {e}")

    with open("test.json", "w") as outfile:
        json.dump(routes, outfile)

    return routes


def start_car_hire_live_session(
    market="DE",
    currency="EUR",
    locale="de-DE",
    pickupplace="50.110924,8.682127-latlong",
    dropoffplace="49.4875,8.466-latlong",
    pickupdatetime="2019-11-12T10:00",
    dropoffdatetime="2019-11-13T10:00",
    driverage="21",
):

    req_url = f"{API_URL}carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}"
    response = requests.post(req_url, headers=HEADERS)

    session_id = response.json()["session_id"]

    return session_id


def get_cheapest_ride(start_city, destination_city, outbound_date, inbound_date):

    # first airport
    session_id = start_car_hire_live_session(
        pickupplace=start_city,
        dropoffplace=destination_city,
        pickupdatetime=f"{outbound_date}T08:00",
        dropoffdatetime=f"{outbound_date}T18:00",
    )
    print(f"session {session_id}")

    req_url = f"{API_URL}/carhire/liveprices/v2/?session_id={session_id}"

    for i in range(5):
        outbound_ride = requests.get(req_url, headers=HEADERS)
        time.sleep(3)

    print(f"status code outbound: {outbound_ride.status_code}")

    with open("rides.json", "w") as outfile:
        json.dump(outbound_ride.json(), outfile)

    # last airport
    session_id = start_car_hire_live_session(
        pickupplace=destination_city,
        dropoffplace=start_city,
        pickupdatetime=f"{inbound_date}T10:00",
        dropoffdatetime=f"{inbound_date}T20:00",
    )
    print(f"session {session_id}")
    req_url = f"{API_URL}/carhire/liveprices/v2/?session_id={session_id}"

    for i in range(5):
        inbound_ride = requests.get(req_url, headers=HEADERS)
        time.sleep(3)

    print(f"status code inbound: {inbound_ride.status_code}")

    with open("rides2.json", "w") as outfile:
        json.dump(outbound_ride.json(), outfile)

    car_connection = []

    try:
        car_connection.append(
            {
                "Start": start_city,
                "Destination": destination_city,
                "Rides": [
                    outbound_ride.json()["cars"][0],
                    inbound_ride.json()["cars"][0],
                ],
            }
        )
    except:
        print("skip dis shit")

    with open("car_connection.json", "w") as outfile:
        json.dump(car_connection, outfile)

    return car_connection


def validate_iata_codes(codes):
    for code in codes:
        if code not in iata_codes:
            codes.remove(code)
    return codes


def do_shit(
    start_city,
    destination_city,
    start_date,
    end_date,
    market="DE",
    currency="EUR",
    locale="de-DE",
):

    start_airports = validate_iata_codes(get_nearest_airports(start_city))
    destination_airports = validate_iata_codes(get_nearest_airports(destination_city))

    print(f"num of start_airports: {len(start_airports)}")
    print(f"num of destination_airports: {len(destination_airports)}")

    cars1 = []
    cars2 = []

    for airport in start_airports:
        print(f"start_airport: {airport}")
        cars1.append(
            get_cheapest_ride(
                get_coordinates_skyscanner(start_city), airport, start_date, end_date
            )
        )
    for airport in destination_airports:
        print(f"destination_airport: {airport}")

        cars2.append(
            get_cheapest_ride(
                airport,
                get_coordinates_skyscanner(destination_city),
                start_date,
                end_date,
            )
        )

    flights = find_flight_routes(
        start_airports, destination_airports, start_date=start_date, end_date=end_date
    )

    return combine_car_plane(cars1, flights, cars2)


def combine_car_plane(cars1, flights, cars2):
    # Route = car1 + flight + car2
    combined_route = []
    cars1 = cars1[0]
    cars2 = cars2[0]

    # print(cars1)
    # print(cars2)
    # print(flights)

    with open("car1.json", "w") as outfile:
        json.dump(cars1, outfile)

    with open("car2.json", "w") as outfile:
        json.dump(cars2, outfile)

    for car1 in cars1:
        for flight in flights:
            for car2 in cars2:
                if not car1:
                    continue
                if not flight:
                    continue
                if not car2:
                    continue
                # try:
                car1_start = car1["Start"]
                car1_destination = car1["Destination"]

                flight_start = flight["Start"]
                flight_destination = flight["Destination"]

                # print(f"car1start: {car1_start}")
                # print(f"car1destination: {car1_destination}")

                # print(f"flightstart: {flight_start}")
                # print(f"flightdestination: {flight_destination}")

                # print(f"car2start: {car2_start}")
                # print(f"car2destination: {car2_destination}")

                # TODO: Add airports back into the flights dict
                # TODO: Consider flight stops
                # for segment in flights["Segments"]["OutboundLegSegments"]:
                #     out_segments.append(segment["OriginStation"])
                # for segment in flights["Segments"]["InboundLegSegments"]:

                car2_start = car2["Start"]
                car2_destination = car2["Destination"]

                if not car1_destination == flight_start:
                    continue
                if not flight_destination == car2_start:
                    continue

                car1_price = (
                    car1["Rides"][0]["price_all_days"]
                    + car1["Rides"][1]["price_all_days"]
                )
                flight_price = flight["Itinerary"]["PricingOptions"]["Price"]
                car2_price = (
                    car2["Rides"][0]["price_all_days"]
                    + car2["Rides"][1]["price_all_days"]
                )

                total_price = car1_price + flight_price + car2_price

                combined_route.append(
                    {
                        "Car1Start": car1_start,
                        "FlightStart": flight_start,
                        "FlightDestination": flight_destination,
                        "Car2Destination": car2_destination,
                        "TotalPrice": total_price,
                    }
                )
                # except Exception as e:
                # print("poof")
                # print(e)

    with open("final1.json", "w") as outfile:
        json.dump(combined_route, outfile)

    # Not sure this will work
    sorted_combined_route = dict(combined_route)
    sorted_combined_route = sorted(combined_route, key=lambda x: x["TotalPrice"])

    with open("final_sorted.json", "w") as outfile:
        json.dump(sorted_combined_route, outfile)

    return sorted_combined_route


# flights = find_flight_routes(["FRA", "STR"], ["TXL", "MUC"])

# combine_car_plane([""], flights, [""])


do_shit(
    start_city="Darmstadt",
    destination_city="Potsdam",
    start_date="2019-11-11",
    end_date="2019-11-20",
)

