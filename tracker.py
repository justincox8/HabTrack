import json
import datetime

def print_habits():
    habits = {}
    with open('habit.json', 'r') as f:
        habits = json.load(f)
    print("HabTrack\n")
    for key, value in habits.items():    
        print(f"{value['habit']}-{value['description']}\nStreak: {value['streak']}\n")

def add_habit(habit, desc):
    try:
        with open('habit.json', 'r') as f:
            habits = json.load(f)
    except json.decoder.JSONDecodeError:
        habits = {}
    new_habit = {len(habits)+1:{
        "habit":habit,
        "description":desc,
        "streak":0
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

def increase_streak():
    habtoincrease = input("Please input the number of the habit you would like to increase: ")
    habits = {}
    with open('habit.json', 'r') as f:
        habits = json.load(f)
    habits[habtoincrease]['streak'] +=1
    with open('habit.json', 'w') as f:
        json.dump(habits, f, indent=4)
    print_habits()
