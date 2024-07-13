from pymongo import MongoClient
from neo4j import GraphDatabase

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"
db_name = "Project"
collection_name = "Clean_data"

# Neo4j connection details
neo_uri = "bolt://localhost:7687"
neo_user = "neo4j"
neo_password = None  # replace with actual password

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Connect to Neo4j
neo_driver = GraphDatabase.driver(neo_uri, auth=(neo_user, neo_password))
session = neo_driver.session()

# Define a function to create Suburb nodes in Neo4j with a label
def create_suburb_node(tx, suburb):
    tx.run("MERGE (:Suburb {suburb: $suburb})", suburb=suburb)

# Define a function to create Place nodes in Neo4j with a label
def create_place_node(tx, name, street, type, postcode):
    tx.run("MERGE (:Place {name: $name, street: $street, type: $type, postcode: $postcode})",
           name=name, street=street, type=type, postcode=postcode)

# Define a function to create relationships between Place and Suburb nodes
def create_relationship(tx, name, suburb, street):
    tx.run("""
        MATCH (p:Place {name: $name, street: $street})
        MATCH (s:Suburb {suburb: $suburb})
        MERGE (p)-[:LOCATED_IN]->(s)
    """, name=name, suburb=suburb , street=street)

# Import data into Neo4j
def import_data(collection):
    results = collection.find({"city": "Messina"})

    for result in results:
        try:
            # Extract required fields
            name = result.get("name")
            street = result.get("street")
            suburb = result.get("suburb")
            postcode = result.get("postcode")
            type_label = result.get("type")

            # Only proceed if the required fields are present
            if name and street and suburb and postcode and type_label:
                session.execute_write(create_place_node, name, street, type_label, postcode)
                session.execute_write(create_suburb_node, suburb)
                session.execute_write(create_relationship, name, suburb, street)
            else:
                print(f"Skipping incomplete data: {result}")

        except Exception as e:
            print(f"Error processing document {result}: {e}")

# Process data from Clean_data collection
import_data(collection)

# Close session and Neo4j driver
session.close()
neo_driver.close()

print("Data imported into Neo4j successfully")