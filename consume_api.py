import requests
import json


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
    adults=2,
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

    session_id = initiate_session(json_params)

    # Poll the result
    req_url = f"{API_URL}flights/search/pricing/v1.0/?session_id={session_id}"
    response = requests.get(req_url, headers=HEADERS)

    print(f"Get Live Prices: HTTP {response.status_code}")


get_live_prices()

