"""
this file is resposible for creating my habit flow database and all the tables it will use
Handles connection to the database

"""

import sqlite3
conn = sqlite3.connect("habitflow.db")


# Database will handle database tasks
class Database:
    def __init__(self,db_name="habitflow.db"): # sets up the database name 
        self.db_name = db_name # saves the database name inside the object
        self.create_tables() # calls the function that creates tables

    def connect(self): # function that opens a connection to the database
        return sqlite3.connect(self.db_name) # opens the database file and returns the connection
    

    def create_tables(self): # function that creates all the tables in the database
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL UNIQUE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY,
            habit_id INTEGER,
            date TEXT,
            status INTEGER
        )
        """)
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_goals (
            id INTEGER PRIMARY KEY,
            habit_id INTEGER,
            goal TEXT,
            date TEXT,
            status INTEGER,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            due_date TEXT,
            status INTEGER
        )
        """)

        conn.commit()
        conn.close()
    
    def migrate(self):
        conn = self.connect()
        cursor = conn.cursor()

        tables = ["habits", "tasks", "goals"]

        for table in tables:

            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]

            if "is_deleted" not in columns:
                cursor.execute(f"""
                ALTER TABLE {table}
                ADD COLUMN is_deleted INTEGER DEFAULT 0
                """)

        conn.commit()
        conn.close()