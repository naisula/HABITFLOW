# HabitFlow 🌸

HabitFlow is a productivity and habit-tracking application built using Python, SQLite, and Streamlit.  
The project was created to help users build consistency by combining habit tracking, goal management, and daily task planning in one system.

Many productivity tools separate habits from daily tasks, making it difficult to connect small daily actions to long-term goals. HabitFlow combines both to create a more organized and practical productivity experience.

---

# Features

## Habit Management
- Add habits
- View habits
- Delete habits
- Track daily habit completion
- Automatic daily reset for habit completion

## Goal Tracking
- Create goals linked to habits
- View goals under their related habits
- Mark goals as complete or incomplete
- Delete goals

## Daily Tasks
- Add daily tasks
- View tasks
- Delete tasks

## Dashboard
- Display total habits, goals, and tasks
- Show daily progress using a progress bar
- Display motivational quotes using an API

## Database Integration
- Store all data using SQLite
- Link goals to habits using foreign keys

---

# Technologies Used

- Python
- SQLite3
- Streamlit
- Git and GitHub
- REST API

---

# Project Structure

```bash
HabitFlow/
│
├── app.py
├── main.py
├── database.py
├── habits.py
├── goals.py
├── tasks.py
├── quotes_api.py
├── habitflow.db
│
├── habits.png
├── goals.png
├── tasks.png
├── flower.png
│
└── README.md