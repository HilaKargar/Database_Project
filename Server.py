from flask import Flask, jsonify, request
from neo4j import GraphDatabase
import mysql.connector
from pymongo import MongoClient
import logging

app = Flask(__name__)
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3308  # Updated port
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root_password'
MYSQL_DB = 'Project'

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = None

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["Database_project"]  # Replace with your database name
bus_collection = db["Bus"]

# Configure logging
logging.basicConfig(level=logging.INFO)

def query_neo4j(query, parameters=None):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run(query, parameters)
        return [{"id": record["id"], "name": record["name"], "type": record["type"], "street": record["street"]} for
                record in result]

def get_liked_places(user_id):
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT place_id FROM user_places WHERE user_id = %s", (user_id,))
    place_ids = cursor.fetchall()
    cursor.close()
    conn.close()
    return [id[0] for id in place_ids]

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username or password not provided"}), 400

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    cursor = conn.cursor()

    cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and user[1] == password:
        liked_places = get_liked_places(user[0])
        return jsonify({"message": "Login successful", "user_id": user[0], "liked_places": liked_places}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route("/signup", methods=["POST"])
def signup():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB)
    cursor = conn.cursor()
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES(%s, %s)", (username, password))
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "User was created"}), 201

@app.route("/places", methods=["GET"])
def get_places():
    data = request.json
    cat = data.get("category")
    if cat == "All":
        results = query_neo4j("MATCH (x:Place) RETURN id(x) AS id, x.name AS name, x.type AS type, x.street AS street")
    else:
        results = query_neo4j(
            "MATCH (x:Place) WHERE x.type = $cat RETURN id(x) AS id, x.name AS name, x.type AS type, x.street AS street",
            {"cat": cat})

    return jsonify(results)

@app.route("/like", methods=["POST"])
def like():
    data = request.json
    user_id = data.get("user_id")
    place_id = data.get("place_id")

    logging.info(f"Received like request: user_id={user_id}, place_id={place_id}")

    if not user_id or not place_id:
        logging.error("User ID or Place ID not provided")
        return jsonify({"error": "User ID or Place ID not provided"}), 400

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_places (user_id, place_id) VALUES (%s, %s)", (user_id, place_id))
        conn.commit()
        logging.info(f"Successfully added like: user_id={user_id}, place_id={place_id}")
    except mysql.connector.Error as err:
        logging.error(f"Error adding like: {err}")
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Place liked"}), 201

@app.route("/unlike", methods=["POST"])
def unlike():
    data = request.json
    user_id = data.get("user_id")
    place_id = data.get("place_id")

    logging.info(f"Received unlike request: user_id={user_id}, place_id={place_id}")

    if not user_id or not place_id:
        logging.error("User ID or Place ID not provided")
        return jsonify({"error": "User ID or Place ID not provided"}), 400

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM user_places WHERE user_id = %s AND place_id = %s", (user_id, place_id))
        conn.commit()
        logging.info(f"Successfully removed like: user_id={user_id}, place_id={place_id}")
    except mysql.connector.Error as err:
        logging.error(f"Error removing like: {err}")
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Place unliked"}), 200

@app.route("/favorites", methods=["GET"])
def favorites():
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400

    place_ids = get_liked_places(user_id)

    if place_ids:
        query = "MATCH (x:Place) WHERE id(x) IN $place_ids RETURN id(x) AS id, x.name AS name, x.type AS type, x.street AS street"
        results = query_neo4j(query, {"place_ids": place_ids})
        return jsonify(results)
    else:
        return jsonify([]), 200

@app.route("/bus_routes", methods=["GET"])
def bus_routes():
    routes = list(bus_collection.find({}, {"_id": 0, "Route_id": 1, "Trip_headsign": 1}))
    return jsonify(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
