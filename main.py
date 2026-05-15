from habits import HabitManager
from tasks import TaskManager
from goals import GoalManager

def main():
    habits = HabitManager()
    tasks = TaskManager()
    goals = GoalManager()


    while True:
        print("\n=== HabitFlow ===")
        print("1. Add Habit")
        print("2. View Habits")
        print("3. Add Task")
        print("4. View Tasks")
        print("5. Add Goal")
        print("6. View Goals")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Habit: ")
            habits.add_habit(name)

        elif choice == "2":
            data = habits.view_habits()
            for row in data:
                print(row)

        elif choice == "3":
            title = input("Task: ")
            due = input("Due date (YYYY-MM-DD): ")
            tasks.add_task(title, due)

        elif choice == "4":
            data = tasks.view_tasks()
            for row in data:
                print(row)

        elif choice == "5":
            break

if __name__ == "__main__":
    main()