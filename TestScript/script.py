from google.transit import gtfs_realtime_pb2
import requests

uri = ""

try:
    with open("env/key.env") as f:
        uri = f.read()
except:
    print("couldn't get API key from env/key.env")
    quit()

if uri == "":
    print("something went wrong getting the API key from env/key/env")
    quit()

uri = "https://sncb-opendata.hafas.de/gtfs/realtime/" + uri

print(uri)
quit()

feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get("URL OF YOUR GTFS-REALTIME SOURCE GOES HERE")
feed.ParseFromString(response.content)
for entity in feed.entity:
    if entity.HasField("trip_update"):
        print(entity.trip_update)
