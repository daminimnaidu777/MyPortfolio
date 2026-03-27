from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# ✅ Get DB URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")
    return psycopg2.connect(DATABASE_URL)

# ✅ Initialize DB safely
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message)
    )

    conn.commit()
    cur.close()
    conn.close()

    return render_template('result.html')

@app.route('/messages')
def messages():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM messages")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('messages.html', data=data)

# ✅ IMPORTANT: Do NOT auto-run init_db on import
# This prevents Gunicorn crash

if __name__ == '__main__':
    init_db()   # runs only locally
    app.run(debug=True)