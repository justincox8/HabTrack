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

def get_user(username):
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    rows = cursor.fetchone()
    cursor.close()
    cnx.close()
    return rows

print(get_user('leila'))