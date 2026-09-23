from flask import Flask, request, jsonify
from collections import deque
import os
import time
import threading

app = Flask(__name__)

signals = deque()
lock = threading.Lock()

@app.route("/", methods=["GET"])
def home():
    return "Arab86Med Webhook is running", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    message = request.get_data(as_text=True).strip()

    if not message:
        return jsonify({"ok": False, "error": "empty message"}), 400

    if not message.startswith("ARAB86MED|"):
        return jsonify({"ok": False, "error": "invalid signal"}), 400

    item = {
        "id": str(time.time_ns()),
        "message": message
    }

    with lock:
        signals.append(item)

    return jsonify({"ok": True, "id": item["id"]}), 200

@app.route("/next", methods=["GET"])
def next_signal():
    with lock:
        if not signals:
            return "NONE", 200

        item = signals.popleft()

    return item["id"] + "|" + item["message"], 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
