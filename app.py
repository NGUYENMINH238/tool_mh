from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Server OK"

@app.route("/login")
def login():
    try:
        with open("login.py", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}", 500