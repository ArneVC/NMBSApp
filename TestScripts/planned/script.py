import pandas as pd
import requests
import zipfile
import os
import shutil
from io import BytesIO

start = input("input start station: ")
if start == "" or start == None:
    print("start station needs to be defined")
    quit()

stop = input("input stop station: ")
if stop == "" or stop == None:
    print("stop station needs to be defined")
    quit()

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

uri = "https://sncb-opendata.hafas.de/gtfs/static/" + uri

response = requests.get(uri)
if response.status_code != 200:
    print("Error downloading GTFS data")
    quit()

dirpath = "gtfs_data"
if os.path.exists(dirpath) and os.path.isdir(dirpath):
    shutil.rmtree(dirpath)
with zipfile.ZipFile(BytesIO(response.content)) as thezip:
    thezip.extractall("gtfs_data")

stops = pd.read_csv("gtfs_data/stops.txt")
stop_times = pd.read_csv("gtfs_data/stop_times.txt")
trips = pd.read_csv("gtfs_data/trips.txt")
routes = pd.read_csv("gtfs_data/routes.txt")


def get_stop_id_by_name(stop_name, stops_df):
    stop_row = stops_df[
        stops_df["stop_name"].str.contains(stop_name, case=False, na=False)
    ]
    if stop_row.empty:
        return None
    return stop_row["stop_id"].values[0]


origin_stop_id = get_stop_id_by_name(start, stops)
destination_stop_id = get_stop_id_by_name(stop, stops)

if origin_stop_id is None or destination_stop_id is None:
    print("Origin or destination station not found")
    quit()

origin_trips = stop_times[stop_times["stop_id"] == origin_stop_id]
destination_trips = stop_times[stop_times["stop_id"] == destination_stop_id]

possible_trips = pd.merge(
    origin_trips, destination_trips, on="trip_id", suffixes=("_origin", "_destination")
)

possible_trips = possible_trips[
    possible_trips["stop_sequence_origin"] < possible_trips["stop_sequence_destination"]
]

possible_trips_with_details = pd.merge(possible_trips, trips, on="trip_id")
possible_trips_with_details = pd.merge(
    possible_trips_with_details, routes, on="route_id"
)

print("Possible trips from origin to destination:")
print(
    possible_trips_with_details[
        [
            "route_id",
            "route_short_name",
            "route_long_name",
            "trip_id",
            "arrival_time_origin",
            "arrival_time_destination",
        ]
    ]
)
