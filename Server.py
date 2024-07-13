from flask import Flask, jsonify, request
from neo4j import GraphDatabase
import mysql.connector

app = Flask(__name__)
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3307  # Updated port
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root_password'
MYSQL_DB = 'modb'

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = None


def query_neo4j(query, parameters=None):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run(query, parameters)
        return [{"name": record["name"], "type": record["type"], "street": record["street"]} for record in result]


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    print(data.get("user"))
    return jsonify({"message": "Logged in"}), 201


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
    username = data.get("user")
    password = data.get("password")
    try:
        cursor.execute("INSERT INTO users (username, password, type) VALUES(%s, %s, %s)", (username, password, 1))
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
        results = query_neo4j("MATCH (x:Place) RETURN x.name AS name, x.type AS type, x.street AS street")
    else:
        results = query_neo4j(
            "MATCH (x:Place) WHERE x.type = $cat RETURN x.name AS name, x.type AS type, x.street AS street",
            {"cat": cat})

    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)