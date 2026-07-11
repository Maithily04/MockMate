import sqlite3
import os

# ----------------------------------
# Create database folder if missing
# ----------------------------------

os.makedirs("database", exist_ok=True)

# ----------------------------------
# Connect to SQLite Database
# ----------------------------------

connection = sqlite3.connect("database/mockmate.db")

cursor = connection.cursor()

# ----------------------------------
# USERS TABLE
# ----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

# ----------------------------------
# RESUME TABLE
# ----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    resume_name TEXT,

    resume_path TEXT,

    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)

)
""")

# ----------------------------------
# QUESTIONS TABLE
# ----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS interview_questions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    question TEXT,

    topic TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)

)
""")

# ----------------------------------
# ANSWERS TABLE
# ----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS answers(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    question_id INTEGER,

    answer TEXT,

    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(question_id)
    REFERENCES interview_questions(id)

)
""")

# ----------------------------------
# FEEDBACK TABLE
# ----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    answer_id INTEGER,

    confidence_score INTEGER,

    strengths TEXT,

    improvements TEXT,

    feedback TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(answer_id)
    REFERENCES answers(id)

)
""")

# ----------------------------------
# INTERVIEW HISTORY
# ----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS interview_history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    total_questions INTEGER,

    correct_answers INTEGER,

    overall_score REAL,

    interview_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(id)

)
""")

# ----------------------------------
# COMMIT
# ----------------------------------

connection.commit()

connection.close()

print("=" * 45)
print(" MockMate Database Created Successfully ")
print("=" * 45)

print("Tables Created:")

print("✔ users")
print("✔ resumes")
print("✔ interview_questions")
print("✔ answers")
print("✔ feedback")
print("✔ interview_history")

print("=" * 45)