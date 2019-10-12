import requests
import json

globalLat = 0
globalLng = 0


def getCoordinates(city):
    url = "https://opencage-geocoder.p.rapidapi.com/geocode/v1/json"
    OPENCAGE_KEY = "aab438e42c9b4046a5aa99173ec4551e"

    querystring = {"language":"en","key":OPENCAGE_KEY,"q":city}

    headers = {
        'x-rapidapi-host': "opencage-geocoder.p.rapidapi.com",
        'x-rapidapi-key': "fdd3d5c155msh470d36197a1bfd6p18b3ccjsn83b2a649205a"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    global globalLat
    global globalLng
    globalLat = response.json()['results'][0]['geometry']['lat']
    globalLng = response.json()['results'][0]['geometry']['lng']

# calls getCoordinates which translates the City Name into coordinates
# takes coordiantes and searchRadius to output nearestAirports
def getNearestAirport(city, searchRadius):
    getCoordinates(city)
    RAPID_API_KEY = "fdd3d5c155msh470d36197a1bfd6p18b3ccjsn83b2a649205a"
    url = "https://cometari-airportsfinder-v1.p.rapidapi.com/api/airports/by-radius"

    querystring = {"radius": searchRadius, "lng": globalLng, "lat": globalLat}

    headers = {
        "x-rapidapi-host": "cometari-airportsfinder-v1.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY,
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    with open("near_airports.json", "w") as outfile:
        json.dump(response.json(), outfile)


getNearestAirport("Mannheim", 50)

