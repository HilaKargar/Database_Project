from pymongo import MongoClient
from neo4j import GraphDatabase

# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"
db_name = "geoapify"
collection_name = "places_clean_data"

# Neo4j connection details
neo_uri = "bolt://localhost:7687"
neo_user = "neo4j"
neo_password = None

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Connect to Neo4j
neo_driver = GraphDatabase.driver(neo_uri, auth=(neo_user, neo_password))
session = neo_driver.session()

# Example query to fetch data from MongoDB
query = {"city": "Messina"}
results = collection.find(query)

# Define a function to create Place nodes in Neo4j with a label
def create_place_node(tx, name, street):
    tx.run("MERGE (:Place {name: $name, street: $street})",
           name=name, street=street)

# Define a function to create Suburb nodes in Neo4j with a label
def create_suburb_node(tx, suburb, postcode):
    tx.run("MERGE (:Suburb {suburb: $suburb, postcode: $postcode})",
           suburb=suburb, postcode=postcode)

# Define a function to create relationships between Place and Suburb nodes
def create_relationship(tx, name, suburb):
    tx.run("""
        MATCH (p:Place {name: $name})
        MATCH (s:Suburb {suburb: $suburb})
        MERGE (p)-[:LOCATED_IN]->(s)
    """, name=name, suburb=suburb)

# Import data into Neo4j
for result in results:
    try:
        # Extract required fields
        name = result.get("name")
        street = result.get("street")
        suburb = result.get("suburb")
        postcode = result.get("postcode")

        # Only proceed if the required fields are present
        if name and street and suburb and postcode:
            session.execute_write(create_place_node, name, street)
            session.execute_write(create_suburb_node, suburb, postcode)
            session.execute_write(create_relationship, name, suburb)
        else:
            print(f"Skipping incomplete data: {result}")

    except Exception as e:
        print(f"Error processing document {result}: {e}")

# Close session and Neo4j driver
session.close()
neo_driver.close()

print("Data imported into Neo4j successfully")
