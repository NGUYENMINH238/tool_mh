from flask import Flask, request, jsonify
import os
import json
import threading
from datetime import datetime

app = Flask(__name__)

VALID_CODE = "1234567890"

ALLOWED_FILES = {
    "thayproxy": "/etc/secrets/thayproxy.py",
    "login": "/etc/secrets/login.py",
    "info": "/etc/secrets/info.py",
    "job": "/etc/secrets/job.py",
}

# =========================
# FILE LƯU THÔNG TIN DEVICE
# =========================

DATA_FILE = "devices.json"
file_lock = threading.Lock()


def load_devices():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_devices(devices):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(devices, f, ensure_ascii=False, indent=2)


# =========================
# TRANG CHỦ
# =========================

@app.route("/")
def home():
    return "Server OK"


# =========================
# LẤY CODE PYTHON
# =========================

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


# =========================
# NHẬN THÔNG TIN MÁY
# =========================

@app.route("/save-device", methods=["POST"])
def save_device():

    # Kiểm tra code
    code = request.args.get("code")

    if code != VALID_CODE:
        return jsonify({
            "success": False,
            "error": "INVALID CODE"
        }), 403

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "error": "NO DATA"
            }), 400

        device_id = str(data.get("device_id", "")).strip()

        if not device_id:
            return jsonify({
                "success": False,
                "error": "MISSING DEVICE ID"
            }), 400

        # Thời gian server nhận
        data["last_seen"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with file_lock:
            devices = load_devices()

            # Cập nhật nếu máy đã tồn tại
            devices[device_id] = data

            save_devices(devices)

        print(f"DEVICE UPDATED: {device_id}", flush=True)

        return jsonify({
            "success": True,
            "message": "DEVICE SAVED",
            "device_id": device_id
        })

    except Exception as e:
        print(f"SAVE DEVICE ERROR: {e}", flush=True)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================
# XEM DANH SÁCH DEVICE
# =========================

@app.route("/devices")
def devices():

    code = request.args.get("code")

    if code != VALID_CODE:
        return "INVALID CODE", 403

    try:
        with file_lock:
            data = load_devices()

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =========================
# CHẠY SERVER
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port
    )
