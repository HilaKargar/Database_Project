from pymongo import MongoClient

mongo_uri = "mongodb://localhost:27017/"
db_name = "Database_project"
collection_source = "Bus"
collection_target = "Bus_clean_data_0"

client = MongoClient(mongo_uri)
db = client[db_name]
collection_source = db[collection_source]
collection_target = db[collection_target]

query = {"Direction": 0}

results = collection_source.find(query, {"_id": 0,
                                         "Route_id": 1,
                                         "Trip_headsign": 1})

inserted_ids = []
for result in results:
    inserted_id = collection_target.insert_one({"Route_id": result["Route_id"],
                                                "Trip_headsign": result["Trip_headsign"],
                                                }).inserted_id
    inserted_ids.append(inserted_id)

print(f"Inserted {len(inserted_ids)} names into {collection_target}")