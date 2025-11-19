# app.py
import threading
import time
import datetime
import json
import os
from flask import Flask, jsonify, send_file

# use the real module names you provided
from face_module import get_face_emotion
from voice_module import get_voice_emotion
from fusion_module import compute_cognitive_state

app = Flask(__name__, static_folder='.')

data_file = "realtime_data.json"
log_file = "cycle_log.txt"

# safe default state so the dashboard /api/state is valid immediately
state = {
    "time": "--:--",
    "face": "neutral",
    "voice": "neu",
    "stress": 0.0,
    "fatigue": 0.0,
    "attention": 0.0,
    "status": "initializing"
}


def collect_cycle():
    """Background loop that captures face + voice once every 60 seconds."""
    while True:
        cycle_start = time.time()
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n🔁 New cycle started: {ts}")

        # defaults on failure
        face_emotion = "neutral"
        voice_emotion = "neu"

        # 1) Capture face emotion
        try:
            print("🧍 Capturing face emotion...")
            face_emotion = get_face_emotion()
            print("  → face:", face_emotion)
        except Exception as e:
            print("❌ Face capture error:", e)

        # 2) Capture voice emotion (5s recording inside module)
        try:
            print("🎤 Capturing voice emotion...")
            voice_emotion = get_voice_emotion()
            print("  → voice:", voice_emotion)
        except Exception as e:
            print("❌ Voice capture error:", e)

        # 3) Fusion via fusion_module.compute_cognitive_state
        try:
            print("🧠 Computing cognitive state via fusion_module...")
            fused = compute_cognitive_state(face_emotion, voice_emotion)
            stress = fused.get("stress", 0.0)
            fatigue = fused.get("fatigue", 0.0)
            attention = fused.get("attention", 0.0)
        except Exception as e:
            print("❌ Fusion error:", e)
            stress, fatigue, attention = 0.5, 0.5, 0.5

        # 4) Update global state
        state.update({
            "time": ts,
            "face": face_emotion,
            "voice": voice_emotion,
            "stress": round(stress, 2),
            "fatigue": round(fatigue, 2),
            "attention": round(attention, 2),
            "status": "active"
        })

        # 5) Persist JSON and append log
        try:
            with open(data_file, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print("❌ Failed to write realtime_data.json:", e)

        try:
            with open(log_file, "a") as log:
                log.write(json.dumps(state) + "\n")
        except Exception as e:
            print("⚠️ Failed to append to log:", e)

        print("✅ Updated state:", state)

        # 6) Sleep until the next full 60s cycle (synchronized)
        elapsed = time.time() - cycle_start
        sleep_time = max(0, 60 - elapsed)
        print(f"⏱ Sleeping {sleep_time:.1f}s until next cycle...")
        time.sleep(sleep_time)


@app.route("/api/state")
def api_state():
    """Return latest cognitive state as JSON."""
    # return in-memory state if file missing (avoids race at startup)
    if os.path.exists(data_file):
        try:
            with open(data_file) as f:
                return jsonify(json.load(f))
        except Exception:
            pass
    return jsonify(state)


@app.route("/")
def serve_dashboard():
    """Serve the dashboard HTML file (must be in project root)."""
    return send_file("dashboard.html")


if __name__ == "__main__":
    print("🚀 Starting app and background capture thread...")
    # start background capture
    t = threading.Thread(target=collect_cycle, daemon=True)
    t.start()
    # run flask
    app.run(debug=True)
