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

    Lat = response.json()['results'][0]['geometry']['lat']
    Long = response.json()['results'][0]['geometry']['lng']

    return f"{Lat},{Long}-latlong"

# calls getCoordinates which translates the City Name into coordinates
# takes coordiantes and searchRadius to output nearestAirports
def getNearestAirport(city, searchRadius):
    airportCoordinates = getCoordinates(city)
    lat = airportCoordinates.partition(',')[0]
    lng = airportCoordinates.partition(',')[2].partition('-')[0]
    RAPID_API_KEY = "fdd3d5c155msh470d36197a1bfd6p18b3ccjsn83b2a649205a"
    url = "https://cometari-airportsfinder-v1.p.rapidapi.com/api/airports/by-radius"

    querystring = {"radius": searchRadius, "lng": lng, "lat": lat}

    headers = {
        "x-rapidapi-host": "cometari-airportsfinder-v1.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY,
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    with open("near_airports.json", "w") as outfile:
        json.dump(response.json(), outfile)


getNearestAirport("Mannheim", 50)

