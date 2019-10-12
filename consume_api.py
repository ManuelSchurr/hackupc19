import requests
import json
import time


API_KEY = "skyscanner-hackupc2019"
API_URL = "https://www.skyscanner.net/g/chiron/api/v1/"


HEADERS = {
    "user-agent": "HackUPC19",
    "Accept": "application/json",
    "api-key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded",
}

# Contains default testing parameters, can - and should - be overwritten
def browse_quotes(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="TXL",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
):

    req_url = f"{API_URL}/flights/browse/browsequotes/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
    response = requests.get(req_url, headers=HEADERS)

    with open("quotes.json", "w") as outfile:
        json.dump(response.json(), outfile)


def browse_routes(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="TXL",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
):
    req_url = f"{API_URL}/flights/browse/browseroutes/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
    response = requests.get(req_url, headers=HEADERS)

    with open("routes.json", "w") as outfile:
        json.dump(response.json(), outfile)


def browse_dates(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="TXL",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
):

    req_url = f"{API_URL}/flights/browse/browsedates/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
    response = requests.get(req_url, headers=HEADERS)

    with open("dates.json", "w") as outfile:
        json.dump(response.json(), outfile)


def browse_dates_grid(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="TXL",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
):

    req_url = f"{API_URL}/flights/browse/browsegrid/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
    response = requests.get(req_url, headers=HEADERS)

    with open("dates_grid.json", "w") as outfile:
        json.dump(response.json(), outfile)


# browse_quotes()
# browse_routes()
# browse_dates()
# browse_dates_grid()


def initiate_session(json_params):
    # Start session
    post_url = f"{API_URL}flights/search/pricing/v1.0/"

    response = requests.post(post_url, json=json_params, headers=HEADERS)
    session_id = response.json()["session_id"]

    print(f"Initiate Session: HTTP {response.status_code}")

    return session_id


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

    with open("raw_dump.json", "w") as outfile:
        json.dump(response.json(), outfile)
    with open("sorted.json", "w") as outfile:
        json.dump(sorted_response, outfile)

    return sorted_response


# get_live_prices()


def find_flight_route(start_airports, destination_airports):
    routes = []
    for start_airport in start_airports:
        for destination_airport in destination_airports:
            print(
                f"Finding best connection. Currently checking: {start_airport} -> {destination_airport}"
            )
            sorted_response = get_live_prices(
                origin_place=start_airport, destination_place=destination_airport
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
                    "From": start_airport,
                    "To": destination_airport,
                    "Itinerary": itinerary,
                    "Legs": legs,
                    "Segments": segments,
                }
            )

    with open("test.json", "w") as outfile:
        json.dump(routes, outfile)

    return routes

def startCarHireLiveSession(
    market = "DE",
    currency = "EUR",
    locale = "de-DE",
    pickupplace  = "50.110924,8.682127-latlong",
    dropoffplace = "49.4875,8.466-latlong",
    pickupdatetime = "2019-11-12T10:00", 
    dropoffdatetime = "2019-11-13T10:00",
    driverage = "21"
):

    req_url = f"{API_URL}/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}"
    response = requests.post(req_url, headers=headers)

    session_id = response.json()["session_id"]

    return session_id

def getCheapestRide():
    session_id = startCarHireLiveSession()

    req_url = f"{API_URL}/carhire/liveprices/v2/?session_id={session_id}"
    response = requests.get(req_url, headers=headers)

    rides = []

    rides.append({"From": "start", "To": "Destination", "Ride": response.json()["cars"][0]})

    with open ("rides.json", "w") as outfile:
        json.dump(rides, outfile)

# find_flight_route(["FRA", "STR"], ["TXL", "MUC"])


def combine_car_plane(cars1, flights, cars2):
    # Route = car1 + flight + car2
    combined_route = []

    for car1 in cars1:
        for flight in flights:
            for car2 in cars2:
                car1_start = car1["Start"]
                flight_start = flight["From"]
                car2_start = car2["Start"]
                car2_destination = car2["Destination"]

                if not car1["DestinationAirport"] == flight_start:
                    continue
                if not flight["DestinationAirport"] == car2_start:
                    continue

                car1_price = car1["Car"]["price_all_days"]
                flight_price = flight["Itinerary"]["PricingOptions"]["Price"]
                car2_price = car2["Car"]["price_all_days"]

                total_price = car1_price + flight_price + car2_price

                combined_route.append(
                    {
                        "Car1Start": car1_start,
                        "FlightStart": flight_start,
                        "Car2Start": car2_start,
                        "Car2Destination": car2_destination,
                        "TotalPrice": total_price,
                    }
                )

    # Not sure this will work
    sorted_combined_route = dict(combined_route)
    sorted_combined_route = sorted(combined_route, key=lambda x: x["TotalPrice"])

    return sorted_combined_route


flights = find_flight_route(["FRA", "STR"], ["TXL", "MUC"])

combine_car_plane([""], flights, [""])

