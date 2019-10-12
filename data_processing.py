import json

dates_grid= "routes.json"

if dates_grid:
    with open(dates_grid, 'r') as f:
        datastore = json.load(f)
QuotesA = datastore['Quotes']
for i in QuotesA:
    print(i['MinPrice'])

# print (test)
# for dates in dates_dict:
#     print(dates['Dates'])