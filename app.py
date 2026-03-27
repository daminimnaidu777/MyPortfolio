from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# CREATE DATABASE
def init_db():
    conn = sqlite3.connect('messages.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    conn = sqlite3.connect('messages.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
                (name, email, message))

    conn.commit()
    conn.close()

    return render_template('result.html', name=name)

@app.route('/messages')
def messages():
    conn = sqlite3.connect('messages.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM messages")
    data = cur.fetchall()

    conn.close()

    return render_template('messages.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)