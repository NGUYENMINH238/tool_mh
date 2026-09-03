from flask import Flask, request

app = Flask(__name__)

VALID_CODE = "1234567890"

ALLOWED_FILES = {
    "thayproxy": "/etc/secrets/thayproxy.py",
    "login": "/etc/secrets/login.py",
    "info": "/etc/secrets/info.py",
    "job": "/etc/secrets/job.py",
}

@app.route("/")
def home():
    return "Server OK"

@app.route("/get-code")
def get_code():
    code = request.args.get("code")
    file_name = request.args.get("file")

    if code != VALID_CODE:
        return "INVALID CODE", 403

    if file_name not in ALLOWED_FILES:
        return "INVALID FILE", 400

    try:
        with open(ALLOWED_FILES[file_name], "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}", 500
