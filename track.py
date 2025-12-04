import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
    
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_user(username,password):
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    cnx.commit()
    cursor.close()
    cnx.close()

cnx = get_connection()
cursor = cnx.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for t in rows:
    print(t)
cursor.close()
cnx.close()

