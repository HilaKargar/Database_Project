import requests
import json
from pymongo import MongoClient

mongo_uri = "mongodb://localhost:27017/"
db_name = "geoapify"
collection_name = "places"

# API for Accommodation
url = "https://api.geoapify.com/v2/places?categories=accommodation&filter=place:519d595c2dc11b2f405914ef5b08cd184340f00101f9015a9a000000000000c00208&limit=40&apiKey=01b1a9639d0c43d489f2af28d2ffb718"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    client = MongoClient("mongodb://localhost:27017")
    db = client["Project"]
    collection = db["Accommodation"]

    if "features" in data:
        collection.insert_many(data["features"])
        print("Data has been inserted into MongoDB")
    else:
        print("No features found in the data")

else:
    print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

# API for Catering
url = "https://api.geoapify.com/v2/places?categories=catering&filter=place:519d595c2dc11b2f405914ef5b08cd184340f00101f9015a9a000000000000c00208&limit=40&apiKey=01b1a9639d0c43d489f2af28d2ffb718"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    client = MongoClient("mongodb://localhost:27017")
    db = client["Project"]
    collection = db["Catering"]

    if "features" in data:
        collection.insert_many(data["features"])
        print("Data has been inserted into MongoDB")
    else:
        print("No features found in the data")

else:
    print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

# API for Commercial
url = "https://api.geoapify.com/v2/places?categories=commercial&filter=place:519d595c2dc11b2f405914ef5b08cd184340f00101f9015a9a000000000000c00208&limit=40&apiKey=01b1a9639d0c43d489f2af28d2ffb718"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    client = MongoClient("mongodb://localhost:27017")
    db = client["Project"]
    collection = db["Commercial"]

    if "features" in data:
        collection.insert_many(data["features"])
        print("Data has been inserted into MongoDB")
    else:
        print("No features found in the data")

else:
    print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

# API for Entertainment
url = "https://api.geoapify.com/v2/places?categories=entertainment&filter=place:519d595c2dc11b2f405914ef5b08cd184340f00101f9015a9a000000000000c00208&limit=40&apiKey=01b1a9639d0c43d489f2af28d2ffb718"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    client = MongoClient("mongodb://localhost:27017")
    db = client["Project"]
    collection = db["Entertainment"]

    if "features" in data:
        collection.insert_many(data["features"])
        print("Data has been inserted into MongoDB")
    else:
        print("No features found in the data")

else:
    print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")