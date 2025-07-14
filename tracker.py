import json
import datetime

def add_habit(habit, desc):
    with open('habit.json', 'r') as f:
        habits = json.load(f)
    new_habit = {len(habits):{
        "habit":habit,
        "description":desc,
        "streak":0
    }}
    habits.update(new_habit)
    with open('habit.json', 'w') as f:
        json.dump(habits, f, indent=4)
    