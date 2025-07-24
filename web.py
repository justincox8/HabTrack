from flask import Flask, render_template, request, redirect, url_for
from tracker import *


app = Flask(__name__)   

@app.route("/")
def index():
    habits = get_habits()
    check_streaks()
    return render_template('index.html', habits=habits)

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
    

