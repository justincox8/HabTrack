from flask import Flask, render_template, request, redirect, url_for, session
from tracker import *
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
    
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

app = Flask(__name__)   
app.secret_key = os.getenv('SECRET_KEY')

@app.route("/", methods=['GET', 'POST'])
@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username,password))
        account = cursor.fetchone()
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            return render_template('index.html', msg='logged in successfully')
        else:
            msg = 'incorrect username/password'

    return render_template('login.html',msg=msg)
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
    return render_template('register.html')
@app.route('/submit', methods=['POST'])
def submit_habit():
    hab = request.form['habname']
    habdescription = request.form['habdescription']
    add_habit(hab, habdescription)
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_habits():
    habit_id = request.form.get('habit_id')
    action = request.form.get('action')

    if action == 'delete':
        delete_habit(habit_id)
    elif action == 'increase':
        increase_streak(habit_id)
    return redirect(url_for('index'))
    

