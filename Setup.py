import time
import subprocess
import docker
import pymysql
from pymongo import MongoClient
import json

# Initialize Docker client
client = docker.from_env()


def start_docker_compose():
    subprocess.run(["docker-compose", "up", "-d"])


def mongo_connection():
    print("Waiting for MongoDB to start...")
    while True:
        try:
            mongo_client = MongoClient("mongodb://localhost:27017/")
            mongo_client.admin.command('ping')
            print("MongoDB is up!")
            break
        except Exception as e:
            print("MongoDB is not ready yet...")
            time.sleep(2)
    return mongo_client


def import_mongo_data(mongo):
    with open("lista-linee.json", "r") as Bus :
        data = json.load(Bus)
    db = mongo["Database_project"]
    db.Bus.insert_many([item for item in data])
    print("MongoDB data imported")


def wait_for_mysql():
    print("Waiting for MySQL to start...")
    while True:
        try:
            connection = pymysql.connect(
                host='localhost',
                port=3308,
                user='root',
                password='root_password'
            )
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            print("MySQL is up!")
            connection.close()
            break
        except pymysql.MySQLError as e:
            print("MySQL is not ready yet...")
            time.sleep(2)


def mysql_init():
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            port=3308,
            user='root',
            password='root_password'
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Project")
        print("Database 'Project' created or already exists")

        # Use the new database
        cursor.execute("USE Project;")
        print("Using database 'Project'")

        # Create the 'users' table
        create_users_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
                )'''
        cursor.execute(create_users_table_query)
        print("Table 'users' created or already exists")

        # Create the 'user_places' table
        create_user_places_table_query = '''
            CREATE TABLE IF NOT EXISTS user_places (
            user_ID INT NOT NULL,
            place_ID INT NOT NULL,
            PRIMARY KEY (user_ID, place_ID),
            CONSTRAINT fk_user
                FOREIGN KEY (user_ID) 
                REFERENCES users(id)
                ON DELETE CASCADE
        )'''
        cursor.execute(create_user_places_table_query)
        print("Table 'user_places' created or already exists")

        # Insert a user into the 'users' table
        insert_user_query = '''
            INSERT INTO users (id,username, password)
            VALUES (1,"test","123")
            '''
        cursor.execute(insert_user_query)
        connection.commit()
        print("User added to 'users' table")

    except pymysql.MySQLError as err:
        print(f"MySQL error: {err}")
    finally:
        cursor.close()
        connection.close()
        print("MySQL connection closed")

#def run_insert_database_script():
   # print("Running insert-database.py script...")
    #subprocess.run(["python3", "convertor.py"])

# Start Docker Compose
#start_docker_compose()

# Wait for MongoDB to be ready and import data
mongo = mongo_connection()
import_mongo_data(mongo)

# Wait for MySQL to be ready and initialize the database
wait_for_mysql()
mysql_init()