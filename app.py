"""
====================================================
MockMate AI
AI Based Mock Interview Platform

Author : Maithily Bhatt
====================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import os
import json
import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.utils import secure_filename

# ==========================================================
# AI UTILS
# ==========================================================

from utils.resume_parser import parse_resume
from utils.question_generator import generate_questions
from utils.feedback import evaluate_answer

# ==========================================================
# FLASK APP
# ==========================================================

app = Flask(__name__)

app.secret_key = "mockmate_secret_key"

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

DATA_FOLDER = os.path.join(
    BASE_DIR,
    "data"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads",
    "resumes"
)

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "mockmate.db"
)

# Create Upload Folder Automatically
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ==========================================================
# ALLOWED FILES
# ==========================================================

ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "txt"
}

# ==========================================================
# INTERVIEW VARIABLES
# ==========================================================

questions = []

current_question = 0

user_answers = []

resume_data = {}

# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn

# ==========================================================
# TRACK VISITED MODULES HELPER
# ==========================================================

def track_page(subject, module_type):
    """
    Logs when a user interacts with learning material 
    to drive the visual progress bar charts dynamically.
    """
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO page_tracking (subject, module_type) VALUES (?, ?)",
            (subject, module_type)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging track metric ({subject} - {module_type}):", e)

# ==========================================================
# CHECK FILE TYPE
# ==========================================================

def allowed_file(filename):

    return (

        "." in filename

        and

        filename.rsplit(
            ".",
            1
        )[1].lower()

        in ALLOWED_EXTENSIONS

    )

# ==========================================================
# LOAD JSON FILES
# ==========================================================

def load_json(filename):

    filepath = os.path.join(

        DATA_FOLDER,

        filename

    )

    if not os.path.exists(filepath):

        return []

    with open(

        filepath,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(file)

# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login")
def login():

    return render_template(
        "login.html"
    )

# ==========================================================
# DASHBOARD (FIXED WITH PROGRESS ENGINE)
# ==========================================================

@app.route("/dashboard")
def dashboard():
    # Initialize safe default structure values so Jinja never breaks
    progress = {
        "python": 0, 
        "html": 0, 
        "css": 0, 
        "javascript": 0, 
        "dsa": 0
    }
    total_attempted = 0
    average_score = 0

    try:
        conn = get_db()
        cursor = conn.cursor()

        # 1. Calculate Interview Performance Metrics
        cursor.execute("SELECT score FROM interview_history")
        records = cursor.fetchall()
        total_attempted = len(records)
        
        if total_attempted > 0:
            average_score = round(sum([row["score"] for row in records]) / total_attempted, 1)

        # 2. Extract Progress Metrics Grouped By Subject Hub
        cursor.execute("SELECT subject, COUNT(DISTINCT module_type) as unique_mods FROM page_tracking GROUP BY subject")
        tracking_rows = cursor.fetchall()
        conn.close()

        for row in tracking_rows:
            subj = str(row["subject"]).lower().strip()
            if subj in progress:
                # Math logic based on 3 distinct resource types per subject
                progress[subj] = int((row["unique_mods"] / 3) * 100)

    except Exception as e:
        print("Dashboard operational fallback error:", e)

    return render_template(
        "dashboard.html",
        total_attempted=total_attempted,
        average_score=average_score,
        progress=progress
    )

# ==========================================================
# RESUME UPLOAD (FIXED ROUTING & REDIRECTS)
# ==========================================================

@app.route("/upload_resume", methods=["GET", "POST"])
def upload_resume():
    global questions
    global current_question
    global user_answers
    global resume_data
    
    if request.method == "GET":
        return redirect(url_for("mock_interview"))

    if "resume" not in request.files:
        flash("Please upload a resume.")
        return redirect(url_for("mock_interview"))

    file = request.files["resume"]

    if file.filename == "":
        flash("No resume selected.")
        return redirect(url_for("mock_interview"))

    if not allowed_file(file.filename):
        flash("Only PDF, DOC, DOCX and TXT files are allowed.")
        return redirect(url_for("mock_interview"))

    filename = secure_filename(file.filename)
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    try:
        file.save(filepath)
    except Exception as e:
        print(e)
        flash("Unable to save resume.")
        return redirect(url_for("mock_interview"))

    try:
        resume_data = parse_resume(filepath)
    except Exception as e:
        print(e)
        flash("Unable to parse resume.")
        return redirect(url_for("mock_interview"))

    skills = resume_data.get("skills", [])

    print("\n========== DETECTED SKILLS ==========")
    for skill in skills:
        print(skill)

    questions = generate_questions(skills)

    if len(questions) == 0:
        questions = [
            "Tell me about yourself.",
            "Explain one project from your resume.",
            "Why should we hire you?",
            "What are your strengths?",
            "Where do you see yourself in 5 years?"
        ]

    print("\n========== GENERATED QUESTIONS ==========\n")
    for i, question in enumerate(questions, start=1):
        print(f"{i}. {question}")

    current_question = 0
    user_answers.clear()

    flash("Resume uploaded successfully!")
    return redirect(url_for("mock_interview"))


# ==========================================================
# VIEW RESUME DETAILS
# ==========================================================

@app.route("/resume_details")
def resume_details():

    global resume_data

    return render_template(
        "resume_details.html",
        resume=resume_data
    )

# ==========================================================
# MOCK INTERVIEW
# ==========================================================

@app.route("/mock_interview")
def mock_interview():

    global questions
    global current_question

    if len(questions) == 0:

        questions = [
            "Tell me about yourself.",
            "Explain your final year project.",
            "Why should we hire you?",
            "What are your strengths?",
            "What is Python?",
            "Explain Object-Oriented Programming.",
            "Difference between List and Tuple.",
            "Explain DBMS.",
            "What is SQL?",
            "Where do you see yourself in 5 years?"
        ]

    if current_question >= len(questions):
        current_question = 0

    return render_template(
        "mock_interview.html",
        question=questions[current_question],
        question_no=current_question + 1,
        total_questions=len(questions)
    )


# ==========================================================
# SUBMIT ANSWER
# ==========================================================

@app.route("/submit_answer", methods=["POST"])
def submit_answer():

    global questions
    global current_question
    global user_answers

    answer = request.form.get(
        "answer",
        ""
    ).strip()

    if answer == "":
        flash("Please enter your answer.")
        return redirect(url_for("mock_interview"))

    user_answers.append(answer)

    result = evaluate_answer(
        questions[current_question],
        answer
    )

    score = result["score"]
    feedback = result["feedback"]
    strengths = result["strengths"]
    improvements = result["improvements"]

    try:
        conn = get_db()
        conn.execute(
            """
            INSERT INTO interview_history (question, answer, score)
            VALUES (?, ?, ?)
            """,
            (questions[current_question], answer, score)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database Error")
        print(e)

    return render_template(
        "result.html",
        question=questions[current_question],
        answer=answer,
        score=score,
        feedback=feedback,
        strengths=strengths,
        improvements=improvements
    )


# ==========================================================
# NEXT QUESTION
# ==========================================================

@app.route("/next_question", methods=["POST"])
def next_question():

    global current_question
    global questions

    current_question += 1

    if current_question >= len(questions):
        flash("🎉 Interview Completed Successfully!")
        current_question = 0
        return redirect(url_for("dashboard"))

    return redirect(url_for("mock_interview"))


# ==========================================================
# RESTART INTERVIEW
# ==========================================================

@app.route("/restart_interview")
def restart_interview():

    global current_question
    global user_answers

    current_question = 0
    user_answers.clear()
    flash("Interview restarted successfully!")
    return redirect(url_for("mock_interview"))

# ==========================================================
# PYTHON HUB
# ==========================================================

@app.route("/python_hub")
def python_hub():
    return render_template("python_hub.html")

@app.route("/python_cheatsheet")
def python_cheatsheet():
    track_page("python", "cheatsheet")
    cheatsheet = load_json("python_cheatsheet.json")
    return render_template("python_cheatsheet.html", cheatsheet=cheatsheet)

@app.route("/python_flashcards")
def python_flashcards():
    track_page("python", "flashcards")
    flashcards = load_json("python_flashcards.json")
    return render_template("python_flashcards.html", flashcards=flashcards)

@app.route("/python_questions")
def python_questions():
    track_page("python", "questions")
    questions = load_json("python_questions.json")
    return render_template("python_questions.html", questions=questions)


# ==========================================================
# HTML HUB
# ==========================================================

@app.route("/html_hub")
def html_hub():
    return render_template("html_hub.html")

@app.route("/html_cheatsheet")
def html_cheatsheet():
    track_page("html", "cheatsheet")
    cheatsheet = load_json("html_cheatsheet.json")
    return render_template("html_cheatsheet.html", cheatsheet=cheatsheet)

@app.route("/html_flashcards")
def html_flashcards():
    track_page("html", "flashcards")
    flashcards = load_json("html_flashcards.json")
    return render_template("html_flashcards.html", flashcards=flashcards)

@app.route("/html_questions")
def html_questions():
    track_page("html", "questions")
    questions = load_json("html_questions.json")
    return render_template("html_questions.html", questions=questions)


# ==========================================================
# CSS HUB
# ==========================================================

@app.route("/css_hub")
def css_hub():
    return render_template("css_hub.html")

@app.route("/css_cheatsheet")
def css_cheatsheet():
    track_page("css", "cheatsheet")
    cheatsheet = load_json("css_cheatsheet.json")
    return render_template("css_cheatsheet.html", cheatsheet=cheatsheet)

@app.route("/css_flashcards")
def css_flashcards():
    track_page("css", "flashcards")
    flashcards = load_json("css_flashcards.json")
    return render_template("css_flashcards.html", flashcards=flashcards)

@app.route("/css_questions")
def css_questions():
    track_page("css", "questions")
    questions = load_json("css_questions.json")
    return render_template("css_questions.html", questions=questions)


# ==========================================================
# JAVASCRIPT HUB
# ==========================================================

@app.route("/javascript_hub")
def javascript_hub():
    return render_template("javascript_hub.html")

@app.route("/js_cheatsheet")
def js_cheatsheet():
    track_page("javascript", "cheatsheet")
    cheatsheet = load_json("js_cheatsheet.json")
    return render_template("js_cheatsheet.html", cheatsheet=cheatsheet)

@app.route("/js_flashcards")
def js_flashcards():
    track_page("javascript", "flashcards")
    flashcards = load_json("js_flashcards.json")
    return render_template("js_flashcards.html", flashcards=flashcards)

@app.route("/js_questions")
def js_questions():
    track_page("javascript", "questions")
    questions = load_json("js_questions.json")
    return render_template("js_questions.html", questions=questions)


# ==========================================================
# DSA HUB
# ==========================================================

@app.route("/dsa_hub")
def dsa_hub():
    return render_template("dsa_hub.html")

@app.route("/dsa_cheatsheet")
def dsa_cheatsheet():
    track_page("dsa", "cheatsheet")
    cheatsheet = load_json("dsa_cheatsheet.json")
    return render_template("dsa_cheatsheet.html", cheatsheet=cheatsheet)

@app.route("/dsa_flashcards")
def dsa_flashcards():
    track_page("dsa", "flashcards")
    flashcards = load_json("dsa_flashcards.json")
    return render_template("dsa_flashcards.html", flashcards=flashcards)

@app.route("/dsa_questions")
def dsa_questions():
    track_page("dsa", "questions")
    questions = load_json("dsa_questions.json")
    return render_template("dsa_questions.html", questions=questions)


# ==========================================================
# INTERVIEW HISTORY
# ==========================================================

@app.route("/history")
def history():
    history_data = []
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, answer, score
            FROM interview_history
            ORDER BY id DESC
        """)
        history_data = cursor.fetchall()
        conn.close()
    except Exception as e:
        print("History Error:", e)

    return render_template("history.html", history=history_data)


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect(url_for("login"))


# ==========================================================
# 404 ERROR
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# ==========================================================
# 500 ERROR
# ==========================================================

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


# ==========================================================
# CREATE DATABASE TABLES
# ==========================================================

def create_table():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Interview performance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interview_history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT,
                score INTEGER
            )
        """)
        
        # Connected metric page tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS page_tracking(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                module_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()
        print("All SQLite Database Engine Tables Connected & Ready.")
    except Exception as e:
        print("Database Schema Initialization Error:", e)


# ==========================================================
# MAIN EXECUTION ENTRYPOINT
# ==========================================================

if __name__ == "__main__":
    create_table()
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5001
    )