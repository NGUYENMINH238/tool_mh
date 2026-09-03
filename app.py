from flask import Flask, request

app = Flask(__name__)

VALID_CODE = "1234567890"

@app.route("/")
def home():
    return "Server OK"

@app.route("/get-code")
def get_code():
    code = request.args.get("code")

    if code != VALID_CODE:
        return "INVALID CODE", 403

    try:
        with open("/login.py", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}", 500
