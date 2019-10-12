import requests
import json


def getNearestAirport(latitude, longitude, searchRadius):
    RAPID_API_KEY = "fdd3d5c155msh470d36197a1bfd6p18b3ccjsn83b2a649205a"
    url = "https://cometari-airportsfinder-v1.p.rapidapi.com/api/airports/by-radius"

    querystring = {"radius": searchRadius, "lng": longitude, "lat": latitude}

    headers = {
        "x-rapidapi-host": "cometari-airportsfinder-v1.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY,
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    with open("near_airports.json", "w") as outfile:
        json.dump(response.json(), outfile)

getNearestAirport(49.412222, 8.71, 50)

