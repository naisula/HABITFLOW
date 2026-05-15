from database import Database

class TaskManager:
    def __init__(self):
        self.db = Database()

    def add_task(self, title, due_date):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tasks (title, due_date, status)
        VALUES (?, ?, 0)
        """, (title, due_date))

        conn.commit()
        conn.close()

    def view_tasks(self):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks")
        data = cursor.fetchall()

        conn.close()
        return data

    def complete_task(self, task_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE tasks
        SET status = 1
        WHERE id = ?
        """, (task_id,))

        conn.commit()
        conn.close()
        
    def delete_task(self, task_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
        """, (task_id,))

        conn.commit()
        conn.close()
        
    def update_task(self, task_id, new_title):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE tasks
        SET title = ?
        WHERE id = ?
        """, (new_title, task_id))

        conn.commit()
        conn.close()