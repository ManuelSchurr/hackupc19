import json

with open("places.json", "r") as f:
    data = json.load(f)


for continent in data["Continents"]:
    print(continent)
