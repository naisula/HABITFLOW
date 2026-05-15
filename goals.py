# This file handles:
# - adding goals
# - viewing goals
# - linking goals to habits
# - completing/uncompleting goals
# - deleting goals

from database import Database
from datetime import date


class GoalManager:

    def __init__(self):

        self.db = Database()

    # ADD GOAL
    def add_goal(self, habit_id, goal):

        conn = self.db.connect()
        cursor = conn.cursor()

        today = str(date.today())

        cursor.execute("""
        INSERT INTO habit_goals
        (habit_id, goal, date, status)
        VALUES (?, ?, ?, 0)
        """, (habit_id, goal, today))

        conn.commit()
        conn.close()

    # VIEW ALL GOALS
    def view_goals(self):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM habit_goals
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    # GET GOALS RELATED TO A SPECIFIC HABIT
    def get_goals_by_habit(self, habit_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM habit_goals
        WHERE habit_id = ?
        """, (habit_id,))

        data = cursor.fetchall()

        conn.close()

        return data

    # DELETE GOAL
    def delete_goal(self, goal_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM habit_goals
        WHERE id = ?
        """, (goal_id,))

        conn.commit()
        conn.close()

    # COMPLETE GOAL
    def complete_goal(self, goal_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE habit_goals
        SET status = 1
        WHERE id = ?
        """, (goal_id,))

        conn.commit()
        conn.close()

    # UNCOMPLETE GOAL
    def uncomplete_goal(self, goal_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE habit_goals
        SET status = 0
        WHERE id = ?
        """, (goal_id,))

        conn.commit()
        conn.close()

    # CHECK IF GOAL IS COMPLETED
    def is_goal_completed(self, goal_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT status
        FROM habit_goals
        WHERE id = ?
        """, (goal_id,))

        data = cursor.fetchone()

        conn.close()

        return data[0] == 1 if data else False
    def update_goal(self, goal_id, new_goal):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE habit_goals
        SET goal = ?
        WHERE id = ?
        """, (new_goal, goal_id))

        conn.commit()
        conn.close()