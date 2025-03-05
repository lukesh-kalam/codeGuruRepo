import sqlite3
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Initialize SQLite database (Insecure: No proper authentication)
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
conn.commit()

# Insecure Login (Vulnerable to SQL Injection)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Vulnerable SQL query (User input is directly injected)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return f"Welcome, {username}!"
        else:
            return "Invalid credentials!"

    return render_template_string('''
        <form method="POST">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

# Insecure User Signup (Stores Plaintext Passwords)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # Password stored in plaintext (Insecure!)

        cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        conn.commit()
        return "User registered successfully!"

    return render_template_string('''
        <form method="POST">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Signup">
        </form>
    ''')

# Cross-Site Scripting (XSS) Vulnerability
@app.route("/greet", methods=["GET"])
def greet():
    name = request.args.get("name", "Guest")
    
    # Vulnerable to XSS (User input directly embedded in HTML)
    return f"<h1>Hello, {name}!</h1>"

# Command Injection Vulnerability
@app.route("/ping", methods=["GET"])
def ping():
    ip = request.args.get("ip", "")
    
    # Insecure command execution (User input directly used in shell command)
    response = os.popen(f"ping -c 1 {ip}").read()
    
    return f"<pre>{response}</pre>"

if __name__ == "__main__":
    app.run(debug=True)
