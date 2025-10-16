import streamlit as st, time, json, datetime
from fusion_module import estimate_cognitive_state
from face_module import get_face_emotion
from voice_module import get_voice_emotion
import pandas as pd

st.set_page_config(page_title="Cognitive Monitoring Dashboard", layout="wide")
st.title("🧠 Cognitive Monitoring & Feedback System")
st.caption("Automatically captures every 2 minutes")

# Store data
if "history" not in st.session_state:
    st.session_state.history = []

placeholder = st.empty()

while True:
    st.markdown("### ⏳ Capturing Face and Voice ...")
    face_emotion = get_face_emotion()
    voice_emotion = get_voice_emotion()

    state = estimate_cognitive_state(face_emotion, voice_emotion)
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    # Save to history
    st.session_state.history.append({
        "time": timestamp,
        "stress": state["stress"],
        "fatigue": state["fatigue"],
        "attention": state["attention"]
    })

    df = pd.DataFrame(st.session_state.history)

    # --- Display current values ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Stress", state["stress"])
    c2.metric("Fatigue", state["fatigue"])
    c3.metric("Attention", state["attention"])

    st.markdown(f"🎭 Face: **{face_emotion}**, 🎙 Voice: **{voice_emotion}**")
    st.write(f"🔹 Sensors → {state['sensors']}")

    # --- Trend Graphs ---
    st.line_chart(df.set_index("time")[["stress", "fatigue", "attention"]])

    st.success(f"✅ Updated at {timestamp}. Next capture in 2 minutes...")
    time.sleep(120)  # 2 minutes
