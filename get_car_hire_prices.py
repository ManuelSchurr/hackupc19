from retrieve_nearest_airports import getCoordinates
import requests
import json


API_KEY = "skyscanner-hackupc2019"
API_URL = "https://www.skyscanner.net/g/chiron/api/v1/"


headers = {"user-agent": "HackUPC19", "Accept": "application/json", "api-key": API_KEY, "userIp": "147.83.201.128", "Content-Type": "application/x-www-form-urlencoded"}

def startCarHireLiveSession(
    market = "DE",
    currency = "EUR",
    locale = "de-DE",
    pickupplace  = "49.4875,8.466-latlong",
    dropoffplace = "51.509865,-0.118092-latlong",
    pickupdatetime = "2019-11-12T10:00", 
    dropoffdatetime = "2019-11-15T10:00",
    driverage = "21"
):

    req_url = f"{API_URL}/carhire/liveprices/v2/{market}/{currency}/{locale}/{pickupplace}/{dropoffplace}/{pickupdatetime}/{dropoffdatetime}/{driverage}"
    response = requests.post(req_url, headers=headers)

    session_id = response.json()["session_id"]

    return session_id