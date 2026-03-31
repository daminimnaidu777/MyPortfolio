from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# DATABASE URL
DATABASE_URL = os.getenv("DATABASE_URL")

# FIX for Render (important)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# CONNECT DATABASE
def get_db():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")
    return psycopg2.connect(DATABASE_URL)

# CREATE TABLE AUTOMATICALLY
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

# RUN ON START
init_db()

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# CONTACT FORM
@app.route('/contact', methods=['POST'])
def contact():
    try:
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

        return render_template('result.html', name=name)

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ADMIN PAGE (UPDATED)
@app.route('/admin')
def admin():
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM messages ORDER BY id DESC")
        data = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('messages.html', data=data)

    except Exception as e:
        return f"❌ Error: {str(e)}"

# OPTIONAL INIT ROUTE (keep if you want)
@app.route('/init')