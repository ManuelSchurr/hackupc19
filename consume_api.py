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
        req_url = f"{API_URL}flights/search/pricing/v1.0/?session_id={session_id}&stops=0&sortType=price&sortOrder=asc&originAirports=FRA&destinationAirports=TXL"
        response = requests.get(req_url, headers=HEADERS)

        status = response.json()["Status"]

        print(f"Get Live Prices: HTTP {response.status_code}")
        print(f"Status:{status}")

        time.sleep(1)

    itineraries = response.json()["Itineraries"]
    legs = response.json()["Legs"]
    segments = response.json()["Segments"]
    places = response.json()["Places"]

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


get_live_prices()


# def find_flight_route(start_airports, destination_airports):
#     for start_airport in start_airports:
#         for destination_airport in destination_airports:
#             pass
