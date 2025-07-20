from flask import Flask, render_template, request, redirect, url_for
from tracker import *


app = Flask(__name__)   

@app.route("/")
def index():
    habits = get_habits()
    return render_template('index.html' ,habits=habits)

@app.route('/submit', methods=['POST'])
def submit_habit():
    hab = request.form['habname']
    habdescription = request.form['habdescription']
    add_habit(hab, habdescription)
    return redirect(url_for('index'))
    

