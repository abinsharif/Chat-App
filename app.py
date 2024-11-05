from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
socketio = SocketIO(app)
connected_users = {}

COLORS = [
    'lime', 'orange', 'blue', 'red', 'purple',
    'brown', 'black', 'green', 'deeppink', 'yellowgreen',
    'gray', 'deepskyblue', 'peru', 'violet', 'crimson',
    'darkolivegreen', 'blueviolet', 'tomato', 'darkblue', 'indigo'
]

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

# Initialize the database
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        color_id = get_next_color_id()
        
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password, color_id) VALUES (?, ?, ?)', 
                             (username, password, color_id))
                conn.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, color_id FROM users WHERE username = ? AND password = ?', 
                         (username, password))
            user = cursor.fetchone()
            
            if user:
                session['user_id'] = user[0]
                session['username'] = username
                session['color_id'] = user[1]
                # Set user as online
                cursor.execute('UPDATE users SET is_online = 1 WHERE id = ?', 
                             (user[0],))
                conn.commit()
                flash('Login successful!', 'success')
                return redirect(url_for('chat'))
            else:
                flash('Invalid username or password.', 'error')
                return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET is_online = 0 WHERE id = ?', 
                         (session['user_id'],))
            conn.commit()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        # Get all messages with sender usernames and colors
        cursor.execute('''
            SELECT messages.message, users.username, messages.timestamp, users.color_id 
            FROM messages 
            JOIN users ON messages.sender_id = users.id 
            ORDER BY messages.timestamp ASC
        ''')
        messages = cursor.fetchall()
        
        # Get online users with their colors
        cursor.execute('SELECT username, color_id FROM users WHERE is_online = 1')
        online_users = cursor.fetchall()
    
    return render_template('chat.html',messages=messages,online_users=online_users,colors=COLORS)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    message = request.form.get('message')
    if message:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (sender_id, message) VALUES (?, ?)',
                         (session['user_id'], message))
            conn.commit()
    
    return redirect(url_for('chat'))

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    username = session.get('username', 'Anonymous')
    connected_users[request.sid] = username
    emit('update_users', list(connected_users.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    if request.sid in connected_users:
        del connected_users[request.sid]
        emit('update_users', list(connected_users.values()), broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    if 'user_id' in session:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (sender_id, message) VALUES (?, ?)',
                         (session['user_id'], data['message']))
            conn.commit()
            
            response = {
                'message': data['message'],
                'username': session['username'],
                'color_id': session['color_id'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            emit('new_message', response, broadcast=True)

@socketio.on('join_room')
def handle_join_room(data):
    join_room(data['room'])
    emit('update_users', get_online_users(), room=data['room'])

@socketio.on('leave_room')
def handle_leave_room(data):
    leave_room(data['room'])
    emit('update_users', get_online_users(), room=data['room'])

def get_online_users():
    pass

if __name__ == '__main__':
    socketio.run(app, host='192.168.0.104', port=1234, debug=True)