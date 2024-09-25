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

feed = gtfs_realtime_pb2.FeedMessage()

try:
    response = requests.get(uri)
    response.raise_for_status()
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        print("\n--- Feed Entity ---")
        print(f"ID: {entity.id}")
        if entity.HasField("trip_update"):
            print("Trip Update:", entity.trip_update)
        elif entity.HasField("vehicle"):
            print("Vehicle Position:", entity.vehicle)
        elif entity.HasField("alert"):
            print("Alert:", entity.alert)

except Exception as e:
    print(f"Error parsing GTFS Realtime data: {e}")
    quit()
