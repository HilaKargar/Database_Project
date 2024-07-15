from pymongo import MongoClient

# Claen Accommodation data
mongo_uri = "mongodb://localhost:27017/"
db_name = "Project"
collection_source = "Accommodation"
collection_target = "Clean_data"

client = MongoClient(mongo_uri)
db = client[db_name]
collection_source = db[collection_source]
collection_target = db[collection_target]

query = {"properties.city": "Messina", "properties.country": "Italy"}

results = collection_source.find(query, {
    "properties.name": 1,
    "properties.city": 1,
    "properties.postcode": 1,
    "properties.suburb": 1,
    "properties.street": 1,
    "properties.datasource.raw.tourism": 1,
    "_id": 0
})

inserted_ids = []
for result in results:
    properties = result.get("properties", {})
    name = properties.get("name", None)
    city = properties.get("city", None)
    suburb = properties.get("suburb", None)
    street = properties.get("street", None)
    postcode = properties.get("postcode", None)
    tourism_type = properties.get("datasource", {}).get("raw", {}).get("tourism", None)

    if name and city and suburb and street and postcode:
        inserted_id = collection_target.insert_one({
            "name": name,
            "city": city,
            "suburb": suburb,
            "street": street,
            "postcode": postcode,
            "type":"Accommodation",
            "subtype": tourism_type
        }).inserted_id
        inserted_ids.append(inserted_id)

print(f"Inserted {len(inserted_ids)} names into {collection_target}")

# Clean Catering data
mongo_uri = "mongodb://localhost:27017/"
db_name = "Project"
collection_source = "Catering"
collection_target = "Clean_data"

client = MongoClient(mongo_uri)
db = client[db_name]
collection_source = db[collection_source]
collection_target = db[collection_target]

query = {"properties.city": "Messina", "properties.country": "Italy"}

results = collection_source.find(query, {"properties.name": 1,
                                         "properties.city": 1,
                                         "properties.postcode": 1,
                                         "properties.suburb": 1,
                                         "properties.street": 1,
                                         "properties.datasource.raw.amenity": 1,
                                         "_id": 0})

inserted_ids = []
for result in results:
    amenity = result["properties"]["datasource"]["raw"]["amenity"] if "datasource" in result["properties"] else None
    inserted_id = collection_target.insert_one({"name": result["properties"]["name"],
                                                "city": result["properties"]["city"],
                                                "suburb": result["properties"]["suburb"],
                                                "street": result["properties"]["street"],
                                                "postcode": result["properties"]["postcode"],
                                                "type": "Catering",
                                                "subtype": amenity
                                                }).inserted_id
    inserted_ids.append(inserted_id)

print(f"Inserted {len(inserted_ids)} names into {collection_target}")

# Clean Commercial data
mongo_uri = "mongodb://localhost:27017/"
db_name = "Project"
collection_source = "Commercial"
collection_target = "Clean_data"

client = MongoClient(mongo_uri)
db = client[db_name]
collection_source = db[collection_source]
collection_target = db[collection_target]

query = {"properties.city": "Messina", "properties.country": "Italy"}

results = collection_source.find(query, {"properties.name": 1,
                                         "properties.city": 1,
                                         "properties.postcode": 1,
                                         "properties.suburb": 1,
                                         "properties.street": 1,
                                         "properties.datasource.raw.shop": 1,
                                         "_id": 0})

inserted_ids = []
for result in results:
    type = result["properties"]["datasource"]["raw"]["shop"] if "datasource" in result["properties"] else None
    inserted_id = collection_target.insert_one({"name": result["properties"]["name"],
                                                "city": result["properties"]["city"],
                                                "suburb": result["properties"]["suburb"],
                                                "street": result["properties"]["street"],
                                                "postcode": result["properties"]["postcode"],
                                                "type": "Commercial",
                                                "subtype": type
                                                }).inserted_id
    inserted_ids.append(inserted_id)

print(f"Inserted {len(inserted_ids)} names into {collection_target}")

# Clean Entertainment data
mongo_uri = "mongodb://localhost:27017/"
db_name = "Project"
collection_source = "Entertainment"
collection_target = "Clean_data"

client = MongoClient(mongo_uri)
db = client[db_name]
collection_source = db[collection_source]
collection_target = db[collection_target]

query = {"properties.city": "Messina", "properties.country": "Italy"}

results = collection_source.find(query, {
    "properties.name": 1,
    "properties.city": 1,
    "properties.postcode": 1,
    "properties.suburb": 1,
    "properties.street": 1,
    "properties.datasource.raw.amenity": 1,
    "_id": 0
})

inserted_ids = []
for result in results:
    properties = result.get("properties", {})
    name = properties.get("name", None)
    city = properties.get("city", None)
    suburb = properties.get("suburb", None)
    street = properties.get("street", None)
    postcode = properties.get("postcode", None)
    amenity = properties.get("datasource", {}).get("raw", {}).get("amenity", None)

    if name and city and suburb and street and postcode:
        inserted_id = collection_target.insert_one({
            "name": name,
            "city": city,
            "suburb": suburb,
            "street": street,
            "postcode": postcode,
            "type" : "Entertainment",
            "subtype": amenity
        }).inserted_id
        inserted_ids.append(inserted_id)

print(f"Inserted {len(inserted_ids)} names into {collection_target}")