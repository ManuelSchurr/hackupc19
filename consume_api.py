import requests
import json


API_KEY = "skyscanner-hackupc2019"
API_URL = "https://www.skyscanner.net/g/chiron/api/v1/"


headers = {"user-agent": "HackUPC19", "Accept": "application/json", "api-key": API_KEY}

# Contains default testing parameters, can - and should - be overwritten
def browse_quotes(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="BER",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
):

    req_url = f"{API_URL}/flights/browse/browsequotes/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
    response = requests.get(req_url, headers=headers)

    with open("quotes.json", "w") as outfile:
        json.dump(response.json(), outfile)


def browse_routes(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="BER",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
):
    req_url = f"{API_URL}/flights/browse/browseroutes/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
    response = requests.get(req_url, headers=headers)

    with open("routes.json", "w") as outfile:
        json.dump(response.json(), outfile)


def browse_dates(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="BER",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
):

    req_url = f"{API_URL}/flights/browse/browsedates/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
    response = requests.get(req_url, headers=headers)

    with open("dates.json", "w") as outfile:
        json.dump(response.json(), outfile)


def browse_dates_grid(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="BER",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
):

    req_url = f"{API_URL}/flights/browse/browsegrid/v1.0/{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
    response = requests.get(req_url, headers=headers)

    with open("dates_grid.json", "w") as outfile:
        json.dump(response.json(), outfile)


browse_quotes()
browse_routes()
browse_dates()
browse_dates_grid()
