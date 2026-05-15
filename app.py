import streamlit as st

from habits import HabitManager
from tasks import TaskManager
from goals import GoalManager
from PIL import Image
from quotes_api import get_quote

# This is the page configuration
st.set_page_config(
    page_title="HabitFlow",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# custom css
st.markdown("""
<style>

/* entire app background */
.stApp {
    background-color: #f7ecef;
}

/* sidebar */
[data-testid="stSidebar"] {
    background-color: #f2dde3;
}

/* main container */
.main .block-container {
    max-width: 700px;
    padding-top: 2rem;
}

/* title */
h1 {
    color: #c76d3a;
    font-size: 52px;
    font-weight: bold;
}

/* subtitles */
h2, h3 {
    color: #6b4f4f;
}

/* text inputs */
div.stTextInput input,
div.stDateInput input {

    background-color: white;
    border-radius: 15px;
    border: none;
    padding: 10px;
    color: black;
}

/* buttons */
div.stButton > button {

    background-color: #e7a6b4;
    color: white;

    border: none;
    border-radius: 15px;

    padding: 10px 25px;

    font-size: 16px;
    font-weight: bold;
}

/* selectbox */
div[data-baseweb="select"] > div {
    background-color: white;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)



habits = HabitManager()
tasks = TaskManager()
goals = GoalManager()


# Header Section: Image next to Title
col_img, col_txt = st.columns([1, 4])

with col_img:
    st.image("flower.png", width=80)

with col_txt:
    st.markdown(
        "<h1>HabitFlow</h1>",
        unsafe_allow_html=True
    )


menu = st.sidebar.selectbox(
    "Menu",
    [
     "Dashboard",
     "Add Habit", 
     "View Habits",
     "Add Goal",
     "View Goals",
     "Add Task", 
     "View Tasks"
     ]
)

if menu == "Dashboard":

    st.header("Dashboard")

    habits_data = habits.view_habits()
    goals_data = goals.view_goals()
    tasks_data = tasks.view_tasks()

    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Habits",
            len(habits_data)
        )

    with col2:
        st.metric(
            "Goals",
            len(goals_data)
        )

    with col3:
        st.metric(
            "Tasks",
            len(tasks_data)
        )

    st.divider()

    
    completed_habits = 0

    for habit in habits_data:

        if habits.is_habit_completed_today(habit[0]):
            completed_habits += 1

    if len(habits_data) > 0:

        progress = completed_habits / len(habits_data)

        st.subheader("Today's Progress")

        st.progress(progress)

        st.write(
            f"{completed_habits} of {len(habits_data)} habits completed today"
        )

    else:
        st.info("No habits added yet.")

    st.divider()
     # aesthetic quote card
    st.subheader("Daily Motivation")

    st.markdown(f"""
    <div style="
        background-color:#f2dde3;
        padding:20px;
        border-radius:20px;
        color:#6b4f4f;
        font-size:18px;
        font-style:italic;
        text-align:center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    ">

    {get_quote()}
    </div>
    """, unsafe_allow_html=True)
    
    


elif menu == "Add Habit":

    st.header("Add Habit")

    habit_name = st.text_input("Enter Habit Name")

    if st.button("Add Habit"):
        habits.add_habit(habit_name)
        st.success("Habit added successfully!")


elif menu == "View Habits":

    st.header("Your Habits")

    habits_data = habits.view_habits()

    for habit in habits_data:

        with st.container():

            col1, col2, col3 = st.columns([1, 6, 1])

            
            with col1:
                st.image("habits.png", width=40)

         
            with col2:

                st.markdown(f"""
                ### {habit[1]}
                """)


                completed_today = habits.is_habit_completed_today(habit[0])

                habit_checked = st.checkbox(
                    "Completed ",
                    value=completed_today,
                    key=f"habit_checkbox_{habit[0]}"
                )

                if habit_checked and not completed_today:

                    habits.complete_habit(habit[0])
                    st.rerun()

                elif not habit_checked and completed_today:

                    habits.uncomplete_habit(habit[0])
                    st.rerun()

                goals_data = goals.get_goals_by_habit(habit[0])

                for goal in goals_data:

                    goal_col1, goal_col2, goal_col3, goal_col4 = st.columns([1, 6, 2, 2])

                    
                    with goal_col1:
                        st.image("goals.png", width=20)

                    
                    with goal_col2:
                        st.write(goal[2])

                    
                    with goal_col3:

                        goal_completed = goals.is_goal_completed(goal[0])

                        goal_checked = st.checkbox(
                            "Done",
                            value=goal_completed,
                            key=f"goal_checkbox_{goal[0]}"
                        )

                        if goal_checked and not goal_completed:

                            goals.complete_goal(goal[0])
                            st.rerun()

                        elif not goal_checked and goal_completed:

                            goals.uncomplete_goal(goal[0])
                            st.rerun()

                    
                    with goal_col4:

                        if st.button(
                            "Del",
                            key=f"goal_delete_{goal[0]}"
                        ):

                            goals.delete_goal(goal[0])

                            st.rerun()
elif menu == "Add Goal":

    st.header("Add Habit Goal")

    habits_data = habits.view_habits()

    habit_options = {
        habit[1]: habit[0]
        for habit in habits_data
    }

    if habit_options:
        selected_habit = st.selectbox(
            "Select Habit",
            list(habit_options.keys())
        )

        goal_text = st.text_input("Enter Goal")

        if st.button("Add Goal"):

            goals.add_goal(
                habit_options[selected_habit],
                goal_text
            )

            st.success("Goal added successfully!")
    else:
        st.warning("Please add a habit first!")


elif menu == "View Goals":

    st.header("Your Goals")

    goals_data = goals.view_goals()

    for goal in goals_data:

        col1, col2 = st.columns([1, 10])

        with col1:
            st.image("goals.png", width=30)

        with col2:
            st.markdown(f"**{goal[2]}**")


elif menu == "Add Task":

    st.header("Add Daily Todo")

    task_title = st.text_input("Task Title")

    due_date = st.date_input("Due Date")

    if st.button("Add Task"):

        tasks.add_task(
            task_title,
            str(due_date)
        )

        st.success("Task added!")


elif menu == "View Tasks":

    st.header("Your Daily Todos")

    data = tasks.view_tasks()

    for task in data:

        col1, col2, col3 = st.columns([1, 6, 1])

        with col1:
            st.image("tasks.png", width=30)

        with col2:
            st.write(task[1])

        with col3:

            if st.button(
                "Del",
                key=f"task_{task[0]}"
            ):

                tasks.delete_task(task[0])

                st.rerun()
