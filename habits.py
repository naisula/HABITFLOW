# This file is responsible for anything habits 
# - adding habits - viewing habits - logging habbits etc

from database import Database
from datetime import date

class HabitManager:
    def __init__(self):
        self.db = Database()

    def add_habit(self, name):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO habits (name) VALUES (?)",
            (name,)
        )

        conn.commit()
        conn.close()

    def view_habits(self):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM habits")
        data = cursor.fetchall()

        conn.close()
        return data

    def log_habit(self, habit_id, status):
        conn = self.db.connect()
        cursor = conn.cursor()

        today = str(date.today())

        cursor.execute("""
        INSERT INTO habit_logs (habit_id, date, status)
        VALUES (?, ?, ?)
        """, (habit_id, today, status))

        conn.commit()
        conn.close()

    def delete_habit(self, habit_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM habits
        WHERE id = ?
        """, (habit_id,))

        conn.commit()
        conn.close()

    def complete_habit(self, habit_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        today = str(date.today())

        cursor.execute("""
        INSERT INTO habit_logs (habit_id, date, status)

        SELECT ?, ?, 1

        WHERE NOT EXISTS (

            SELECT 1
            FROM habit_logs
            WHERE habit_id = ?
            AND date = ?

        )
        """, (habit_id, today, habit_id, today))

        conn.commit()
        conn.close()

    def is_habit_completed_today(self, habit_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        today = str(date.today())

        cursor.execute("""
        SELECT * FROM habit_logs
        WHERE habit_id = ?
        AND date = ?
        """, (habit_id, today))

        data = cursor.fetchone()

        conn.close()

        return data is not None
    def uncomplete_habit(self, habit_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        today = str(date.today())

        cursor.execute("""
        DELETE FROM habit_logs
        WHERE habit_id = ?
        AND date = ?
        """, (habit_id, today))

        conn.commit()
        conn.close()
def update_habit(self, habit_id, new_name):

    conn = self.db.connect()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE habits
    SET name = ?
    WHERE id = ?
    """, (new_name, habit_id))

    conn.commit()
    conn.close() 