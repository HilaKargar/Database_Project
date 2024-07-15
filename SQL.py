import mysql.connector
from mysql.connector import errorcode, cursor

# Database configuration
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3308  # Updated port
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root_password'

conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Project")

conn.database = "Project"

create_users_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
        )'''
cursor.execute(create_users_table_query)
print("Table 'users' created successfully.")

insert_user_query = '''
    INSERT INTO users (id,username, password)
    VALUES (1,"test","123")
    '''

cursor.execute(insert_user_query)
conn.commit()
print("Sample data inserted successfully.")

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
print("Table 'user_places' created successfully.")




