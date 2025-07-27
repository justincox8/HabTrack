import json
import datetime
import os

def print_habits():
    habits = {}
    with open('habit.json', 'r') as f:
        habits = json.load(f)
    print("HabTrack\n")
    for key, value in habits.items():    
        print(f"{key}. {value['habit']}-{value['description']}\nStreak: {value['streak']}\n")

def get_habits():
    if not os.path.isfile('habit.json'):
        habits = {}
        with open('habit.json', 'w') as f:
            json.dump(habits, f, indent=4)
    try:
        with open('habit.json', 'r') as f:
            habits = json.load(f)
    except json.decoder.JSONDecodeError:
        habits = {}
    return habits

def add_habit(habit, desc):
    date = datetime.datetime.now()
    try:
        with open('habit.json', 'r') as f:
            habits = json.load(f)
    except json.decoder.JSONDecodeError:
        habits = {}
    new_habit = {len(habits)+1:{
        "habit":habit,
        "description":desc,
        "streak":0,
        "day": date.day
        
    }}
    habits.update(new_habit)
    with open('habit.json', 'w') as f:
        json.dump(habits, f, indent=4)
    print_habits()

def delete_habit(delhabit):
    habits = {}
    with open('habit.json', 'r') as f:
        habits = json.load(f)
    keytodelete = 'x'
    for key, value in habits.items():
        if value['habit'] == delhabit:
            keytodelete = key
    if keytodelete != 'x':
        del habits[keytodelete]
    with open('habit.json', 'w') as f:
        json.dump(habits, f, indent=4)
    print_habits()

def increase_streak(habittoincrease):
    habits = {}
    date = datetime.datetime.day
    with open('habit.json', 'r') as f:
        habits = json.load(f)

    for key, value in habits.items():
        if value['habit'] == habittoincrease and value['day'] != date:
            habits[key]['streak'] +=1
    with open('habit.json', 'w') as f:
        json.dump(habits, f, indent=4)
    print_habits()

def check_streaks():
    date = datetime.datetime.now()
    day = date.day
    month = date.month
    try:
        with open('habit.json', 'r') as f:
            habits = json.load(f)
    except json.decoder.JSONDecodeError:
        habits = {}
    for key, value in habits.items():
        if month == 4 or month == 6 or month == 9 or month == 11:
            if value['day'] == 28 and day > 1:
                del habits[key]
            if value['day'] == 29 and day > 2:
                del habits[key]
            if value['day'] == 30 and day > 3:
                del habits[key]
        elif month == 2:
            if value['day'] == 26 and day > 1:
                del habits[key]
            if value['day'] == 27 and day > 2:
                del habits[key]
            if value['day'] == 28 and day > 3:
                del habits[key]
        else:
            if value['day'] == 29 and day > 1:
                del habits[key]
            if value['day'] == 30 and day > 2:
                del habits[key]
            if value['day'] == 31 and day > 3:
                del habits[key]
        if day > (value['day'] + 3):
            del habits[key]
    with open('habit.json', 'w') as f:
        json.dump(habits, f, indent=4)

