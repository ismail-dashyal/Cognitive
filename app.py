import threading
import time
from flask import Flask, jsonify, send_file
from face_emotion import get_face_emotion
from voice_emotion import get_voice_emotion
import random, datetime, json, os

app = Flask(__name__, static_folder='.')

data_file = "realtime_data.json"
state = {}

# -------- BACKGROUND DATA CAPTURE LOOP --------
def collect_data():
    while True:
        print("🔁 Capturing new data...")
        try:
            face_emotion = get_face_emotion()
            voice_emotion = get_voice_emotion()

            # Basic rule-based fusion logic
            stress = random.uniform(0.6, 1.0) if face_emotion in ["angry", "fear"] else random.uniform(0.2, 0.6)
            fatigue = random.uniform(0.5, 0.9) if face_emotion in ["sad", "neutral"] else random.uniform(0.2, 0.5)
            attention = max(0, min(1, 1 - (stress + fatigue) / 2))

            state.update({
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "face": face_emotion,
                "voice": voice_emotion,
                "stress": round(stress, 2),
                "fatigue": round(fatigue, 2),
                "attention": round(attention, 2)
            })

            # Save to file
            with open(data_file, "w") as f:
                json.dump(state, f, indent=2)

            print("✅ Updated state:", state)

        except Exception as e:
            print("❌ Error while capturing data:", e)

        time.sleep(60)  # ⏱ every 1 minute

# -------- API ENDPOINTS --------
@app.route("/api/state")
def api_state():
    if not os.path.exists(data_file):
        return jsonify({"error": "No data yet"})
    with open(data_file) as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/")
def serve_dashboard():
    return send_file("dashboard.html")

# -------- START APP --------
if __name__ == "__main__":
    threading.Thread(target=collect_data, daemon=True).start()
    app.run(debug=True)
