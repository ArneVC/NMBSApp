import pandas as pd
import requests
import zipfile
import os
from io import BytesIO

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

# TODO: make sure folder is cleared
with zipfile.ZipFile(BytesIO(response.content)) as thezip:
    thezip.extractall("gtfs_data")
