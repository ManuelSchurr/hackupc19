from retrieve_nearest_airports import getCoordinates
import requests
import json
import time


API_KEY = "skyscanner-hackupc2019"
API_URL = "https://www.skyscanner.net/g/chiron/api/v1/"


headers = {"user-agent": "HackUPC19", "Accept": "application/json", "api-key": API_KEY}

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

   
getCheapestRide()