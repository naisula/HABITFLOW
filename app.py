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
        st.metric("Habits",len(habits_data))

    with col2:
        st.metric("Goals",len(goals_data))

    with col3:
        st.metric("Tasks",len(tasks_data))

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

    habit_name = st.text_input("Enter Habit ")

    if st.button("Add Habit"):
        habits.add_habit(habit_name)
        st.success("Habit added successfully!")


elif menu == "View Habits":

    st.header("Habits")

    @st.dialog("Delete Habit")
    def delete_habit_dialog():

        habit_id = st.session_state["delete_habit_id"]
        habit_name = st.session_state["delete_habit_name"]

        st.write(f"Are you sure you want to delete **{habit_name}**?")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Yes"):

                habits.delete_habit(habit_id)

                st.session_state["delete_habit_id"] = None
                st.session_state["delete_habit_name"] = None

                st.rerun()

        with c2:
            if st.button("No"):

                st.session_state["delete_habit_id"] = None
                st.session_state["delete_habit_name"] = None

                st.rerun()

    habits_data = habits.view_habits()

    for habit in habits_data:
    
        with st.container():

            col1, col2, col3 = st.columns([1, 6, 1])

            
            with col1:
                st.image("habits.png", width=40)

         
            with col2:

                st.markdown(f"### {habit[1]}")

                with st.expander("Edit"):

                    updated_name = st.text_input(
                        "New Habit",
                        value=habit[1],
                        key=f"edit_habit_{habit[0]}"
                    )

                    if st.button("Save Habit",key=f"save_habit_{habit[0]}"):

                        habits.update_habit(
                            habit[0],
                            updated_name
                        )

                        st.success("Habit updated!")

                        st.rerun()



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

                        with st.expander("Edit Goal"):

                            updated_goal = st.text_input(
                                "New Goal",
                                value=goal[2],
                                key=f"edit_goal_{goal[0]}"
                            )

                            if st.button(
                                "Save Goal",
                                key=f"save_goal_{goal[0]}"
                            ):

                                goals.update_goal(
                                    goal[0],
                                    updated_goal
                                )

                                st.success("Goal updated!")

                                st.rerun()

                    
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

                        if f"confirm_delete_goal_{goal[0]}" not in st.session_state:
                            st.session_state[f"confirm_delete_goal_{goal[0]}"] = False

                        if not st.session_state[f"confirm_delete_goal_{goal[0]}"]:

                            if st.button(
                                "Del",
                                key=f"goal_delete_{goal[0]}"
                            ):

                                st.session_state[f"confirm_delete_goal_{goal[0]}"] = True
                                st.rerun()

                        else:

                            st.warning("Are you sure you want to delete this goal?")

                            c1, c2 = st.columns(2)

                            with c1:
                                if st.button("Yes", key=f"yes_goal_{goal[0]}"):

                                    goals.delete_goal(goal[0])

                                    st.session_state[f"confirm_delete_goal_{goal[0]}"] = False

                                    st.rerun()

                            with c2:
                                if st.button("No", key=f"no_goal_{goal[0]}"):

                                    st.session_state[f"confirm_delete_goal_{goal[0]}"] = False

                                    st.rerun()

            with col3:

                if st.button("Del", key=f"delete_habit_{habit[0]}"):

                    st.session_state["delete_habit_id"] = habit[0]
                    st.session_state["delete_habit_name"] = habit[1]

                    delete_habit_dialog()

                
                
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

    @st.dialog("Delete Goal")
    def delete_goal_dialog():

        goal_id = st.session_state["delete_goal_id"]
        goal_name = st.session_state["delete_goal_name"]

        st.write(f"Are you sure you want to delete **{goal_name}**?")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Yes"):

                goals.delete_goal(goal_id)

                st.session_state["delete_goal_id"] = None
                st.session_state["delete_goal_name"] = None

                st.rerun()

        with c2:
            if st.button("No"):

                st.session_state["delete_goal_id"] = None
                st.session_state["delete_goal_name"] = None

                st.rerun()

    goals_data = goals.view_goals()

    for goal in goals_data:

        with st.container():

            col1, col2, col3 = st.columns([1, 8, 2])

            with col1:
                st.image("goals.png", width=30)

            with col2:

                st.markdown(f"**{goal[2]}**")

                with st.expander("Edit Goal"):

                    updated_goal = st.text_input(
                        "New Goal",
                        value=goal[2],
                        key=f"edit_goal_page_{goal[0]}"
                    )

                    if st.button(
                        "Save Goal",
                        key=f"save_goal_page_{goal[0]}"
                    ):

                        goals.update_goal(
                            goal[0],
                            updated_goal
                        )

                        st.success("Goal updated!")

                        st.rerun()

            with col3:

                if st.button("Del", key=f"delete_goal_page_{goal[0]}"):

                    st.session_state["delete_goal_id"] = goal[0]
                    st.session_state["delete_goal_name"] = goal[2]

                    delete_goal_dialog()


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

    @st.dialog("Delete Task")
    def delete_task_dialog():

        task_id = st.session_state["delete_task_id"]
        task_name = st.session_state["delete_task_name"]

        st.write(f"Are you sure you want to delete **{task_name}**?")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Yes"):

                tasks.delete_task(task_id)

                st.session_state["delete_task_id"] = None
                st.session_state["delete_task_name"] = None

                st.rerun()

        with c2:
            if st.button("No"):

                st.session_state["delete_task_id"] = None
                st.session_state["delete_task_name"] = None

                st.rerun()

    data = tasks.view_tasks()

    for task in data:

        with st.container():

            col1, col2, col3 = st.columns([1, 6, 2])

            with col1:
                st.image("tasks.png", width=30)

            with col2:

                st.write(task[1])

                with st.expander("Edit Task"):

                    updated_task = st.text_input(
                        "New Task",
                        value=task[1],
                        key=f"edit_task_{task[0]}"
                    )

                    if st.button(
                        "Save Task",
                        key=f"save_task_{task[0]}"
                    ):

                        tasks.update_task(
                            task[0],
                            updated_task
                        )

                        st.success("Task updated!")

                        st.rerun()

            with col3:

                if st.button("Del", key=f"task_{task[0]}"):

                    st.session_state["delete_task_id"] = task[0]
                    st.session_state["delete_task_name"] = task[1]

                    delete_task_dialog()