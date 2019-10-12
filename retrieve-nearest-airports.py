import requests
import json

url = "https://cometari-airportsfinder-v1.p.rapidapi.com/api/airports/by-radius"

querystring = {"radius":"50","lng":"8.71","lat":"49.412222"}

headers = {
    'x-rapidapi-host': "cometari-airportsfinder-v1.p.rapidapi.com",
    'x-rapidapi-key': "fdd3d5c155msh470d36197a1bfd6p18b3ccjsn83b2a649205a"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

with open("near_airports.json", "w") as outfile:
        json.dump(response.json(), outfile)