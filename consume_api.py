import requests
import json


API_KEY = "skyscanner-hackupc2019"
API_URL = "https://www.skyscanner.net/g/chiron/api/v1/flights/browse/browsequotes/v1.0/"


headers = {"user-agent": "HackUPC19", "Accept": "application/json", "api-key": API_KEY}


def get_cheapest_fare(
    country="DE",
    currency="EUR",
    locale="DE",
    origin_place="FRA",
    destination_place="BER",
    outbound_partial_date="2019-11-11",
    inbound_partial_date="2019-11-12",
):

    req_url = f"{API_URL}{country}/{currency}/{locale}/{origin_place}/{destination_place}/{outbound_partial_date}/{inbound_partial_date}/"
    response = requests.get(req_url, headers=headers)
    return response.json()


print(get_cheapest_fare())

