from pymongo import MongoClient

mongo_uri = "mongodb://localhost:27017/"
db_name = "Project"
collection_source = "Entertainment"
collection_target = "Entertainment_clean_data"

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
    amenity = result["properties"]["datasource"]["raw"]["amenity"] if "datasource.raw" in result["properties"] else None
    inserted_id = collection_target.insert_one({"name": result["properties"]["name"],
                                                "city": result["properties"]["city"],
                                                "suburb": result["properties"]["suburb"],
                                                "street": result["properties"]["street"],
                                                "postcode": result["properties"]["postcode"],
                                                "amenity": amenity
                                                }).inserted_id
    inserted_ids.append(inserted_id)

print(f"Inserted {len(inserted_ids)} names into {collection_target}")


