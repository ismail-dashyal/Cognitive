import os, time, threading, json, datetime, random
from flask import Flask, jsonify, send_from_directory
from face_emotion import get_face_emotion
from voice_emotion import get_voice_emotion

DATA_FILE = "realtime_data.json"

app = Flask(__name__, static_folder=".")

# ---------- EMOTION CAPTURE LOGIC ----------
def update_data():
    while True:
        print("🧠 Capturing new data...")
        try:
            face_emo = get_face_emotion()
            voice_emo = get_voice_emotion()

            # Map emotions → stress/fatigue/attention (simple fusion)
            stress = random.uniform(0.3, 0.9) if face_emo != "happy" else random.uniform(0.1, 0.4)
            fatigue = random.uniform(0.2, 0.8) if voice_emo != "neu" else random.uniform(0.1, 0.5)
            attention = 1 - (stress + fatigue) / 2
            attention = max(0, min(1, attention))

            data = {
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "face": face_emo,
                "voice": voice_emo,
                "stress": round(stress, 2),
                "fatigue": round(fatigue, 2),
                "attention": round(attention, 2)
            }
            with open(DATA_FILE, "w") as f:
                json.dump(data, f)
            print("✅ Updated data:", data)
        except Exception as e:
            print("❌ Error updating data:", e)
        time.sleep(120)  # every 2 minutes

# ---------- FLASK API ----------
@app.route("/api/state")
def api_state():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "No data yet"})
    with open(DATA_FILE) as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/")
def serve_dashboard():
    return send_from_directory(".", "dashboard.html")

# ---------- MAIN ----------
if __name__ == "__main__":
    t = threading.Thread(target=update_data, daemon=True)
    t.start()
    app.run(debug=True)
