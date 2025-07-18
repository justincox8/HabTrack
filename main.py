from tracker import *


def main():
    print_habits()
    while True:    
        choice=input("1. Add a Habit\n2. Increase habit streak\n3. Delete Habit\n4. Exit\nEnter Choice: ")
        if choice=='1':
            habit=input('Habit name: ')
            desc=input('Habit description: ')
            add_habit(habit, desc)
        elif choice =='2':
            increase_streak()
        elif choice == '3':
            habit=input('Please enter habit to delete: ')
            delete_habit(habit)
        else:
            break


main()