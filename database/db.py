import sqlite3
from flask import g

# Database file path
DATABASE = "database/mockmate.db"


def get_db():
    """
    Returns the database connection.
    Creates a new connection if one doesn't exist.
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Return rows as dictionaries

    return g.db


def close_db(error=None):
    """
    Closes the database connection.
    Called automatically after every request.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """
    Creates the required tables if they don't already exist.
    """
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            score INTEGER,
            feedback TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    db.commit()
    db.close()


def init_app(app):
    """
    Register database functions with Flask.
    """
    app.teardown_appcontext(close_db)