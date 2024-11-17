# utils.py

from flask import session, redirect, url_for, flash
from functools import wraps
import sqlite3

COLORS = [
    'lime', 'orange', 'blue', 'red', 'purple',
    'brown', 'black', 'green', 'deeppink', 'yellowgreen',
    'gray', 'deepskyblue', 'peru', 'violet', 'crimson',
    'darkolivegreen', 'blueviolet', 'tomato', 'darkblue', 'indigo'
]

def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_next_color_id():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(color_id) FROM users')
        last_color = cursor.fetchone()[0]
        if last_color is None:
            return 1
        return (last_color % len(COLORS)) + 1
    
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_online BOOLEAN DEFAULT 0,
                color_id INTEGER DEFAULT 1
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users (id)
            )
        ''')
        conn.commit()