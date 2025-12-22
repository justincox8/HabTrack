from flask import Flask, render_template, request, redirect, url_for, session
from track import *
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import re
import psycopg2
from psycopg2.extras import RealDictCursor
load_dotenv()

def set_password(password):
   return generate_password_hash(password, method='scrypt', salt_length=16)

def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)
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
        cursor = cnx.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        account = cursor.fetchone()
        if account == None:
            return(render_template('login.html', error="wrong username or password"))
        if check_password(account['password'], password) == True:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            print(session['id'])
            print(get_habits(session['id']))
            return render_template('index.html', msg='logged in successfully', habits=get_habits(account['id']))
        else:
            msg = 'incorrect username/password'

    return render_template('login.html',msg=msg)
@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cnx = get_connection()
        cursor = cnx.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
            print('account exists')
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
            print('letters or nums')
        elif not username or not password:
            msg = 'Please fill out the form!'
            print('blank')
        else:
            print('made it')
            password = set_password(password)
            cursor.execute("INSERT INTO users (username,password) VALUES (%s, %s)", (username, password))
            cnx.commit()
            msg = 'Logged in succsesfully'
            cursor.close()
            return redirect(url_for('login'))
    return render_template('register.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def index():
    return render_template('index.html',habits=get_habits(session['id']))
@app.route('/submit', methods=['POST'])
def submit_habit():
    hab = request.form['habname']
    habdescription = request.form['habdescription']
    add_habit(session['id'],hab, habdescription)
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_habits():
    habit_id = request.form.get('habit_id')
    action = request.form.get('action')

    habit_id = int(habit_id)
    user_id = int(session['id'])
    if action == 'delete':
        delete_habit(user_id,habit_id)
    elif action == 'increase':
        increase_streak(habit_id, user_id)
    return redirect(url_for('index'))
    

