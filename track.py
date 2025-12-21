import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()




def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        dbname=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT"),
        sslmode="require"
    )

def create_user(username,password):
    cnx = get_connection()
    cursor = cnx.cursor(cursor_factory=RealDictCursor)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    cnx.commit()
    cursor.close()
    cnx.close()

def get_user(username):
    cnx = get_connection()
    cursor = cnx.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    rows = cursor.fetchone()
    cursor.close()
    cnx.close()
    return rows

def get_habits(user_id):
    cnx = get_connection()
    cursor = cnx.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM habits WHERE user_id=%s", (user_id,))
    row = cursor.fetchall()
    return row

def add_habit(user_id, habit, description):
    cnx = get_connection()
    cursor = cnx.cursor(cursor_factory=RealDictCursor)
    cursor.execute("INSERT INTO habits (user_id, habit, descr, streak, last_day) VALUES (%s, %s, %s, %s, %s)", (user_id, habit, description, 0, datetime.now().date()))
    cnx.commit()
    cursor.close()
    cnx.close()

def delete_habit(user_id, habit_id):
    cnx = get_connection()
    cursor = cnx.cursor(cursor_factory=RealDictCursor)
    cursor.execute("DELETE FROM habits WHERE user_id=%s AND id=%s", (user_id, habit_id))
    cnx.commit()
    cursor.close()
    cnx.close()

def increase_streak(habit_id, user_id):
    today = datetime.today().date()
    cnx = get_connection()
    cursor = cnx.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT streak, last_day FROM habits WHERE user_id=%s AND id=%s", (user_id, habit_id))
    row = cursor.fetchone()
    if row:
        streak = row['streak']
        last_day =row['last_day']
        if last_day != today:
            cursor.execute("UPDATE habits SET streak=%s, last_day=%s WHERE user_id=%s AND id=%s", (streak+1, today, user_id,habit_id))
            cnx.commit()
        else:
            print("cant increase streak twice in one day")
    cursor.close()
    cnx.close()
