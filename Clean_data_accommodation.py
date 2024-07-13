from pymongo import MongoClient

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
