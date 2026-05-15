-- SQLite
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Habits(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE
);

INSERT OR IGNORE INTO Habits(Name)
VALUES
    ("Wake up Early"),
    ("Workout"),
    ("Drink a glass of water"),
    ("Read a book"),
    ("Sleep 8 hours"),
    ("Brush twice a day"),
    ("Journal")

CREATE TABLE IF NOT EXISTS habit_logs(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Habit_Id INTEGER,
    Date TEXT,
    Status INTEGER,
    FOREIGN KEY (Habit_Id) REFERENCES Habits(Id)


);

CREATE TABLE IF NOT EXISTS Tasks(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT ,
    Due_date TEXT,
    Status INTEGER

);



