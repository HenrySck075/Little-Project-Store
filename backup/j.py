import json, requests
a = json.loads(requests.get("https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json").text)
b={}
for i in a["elements"]:
    b[i["symbol"]]=i["number"]

json.dump(b,open("a.json","w"))
