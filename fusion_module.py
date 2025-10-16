import random
import time

# --- Simulated sensor inputs (HRV, typing speed, EDA) ---
def get_simulated_signals():
    """
    Generate simulated physiological and behavioral values.
    These mimic HRV (Heart Rate Variability), typing speed, and EDA (Electrodermal Activity).
    """
    hrv = random.uniform(50, 90)            # HRV in ms (higher = relaxed)
    typing_speed = random.uniform(200, 350) # chars/min (higher = alert)
    eda = random.uniform(0.1, 0.6)          # microsiemens (higher = stress)
    return {"hrv": hrv, "typing_speed": typing_speed, "eda": eda}


# --- Fusion logic ---
def estimate_cognitive_state(face_emotion, voice_emotion):
    """
    Combines face emotion, voice emotion, and simulated sensors
    to estimate overall cognitive state (stress, fatigue, attention).
    """

    # Emotion → stress/fatigue weight maps
    emotion_to_stress = {
        "angry": 0.9, "fear": 0.8, "sad": 0.7,
        "neutral": 0.3, "happy": 0.2, "surprise": 0.5, "calm": 0.2, "neu": 0.3
    }
    emotion_to_fatigue = {
        "neutral": 0.4, "sad": 0.8, "angry": 0.6,
        "happy": 0.2, "surprise": 0.3, "fear": 0.7, "calm": 0.3, "neu": 0.4
    }

    # Base emotion-based values
    stress = emotion_to_stress.get(voice_emotion, 0.5)
    fatigue = emotion_to_fatigue.get(face_emotion, 0.5)

    # Add simulated sensor modifiers
    sensors = get_simulated_signals()

    # HRV: higher → lower stress
    stress += (0.5 - sensors["hrv"] / 200)
    # EDA: higher → higher stress
    stress += sensors["eda"]

    # Typing speed: slower typing → more fatigue
    fatigue += (350 - sensors["typing_speed"]) / 400

    # Clamp between 0–1
    stress = min(max(stress, 0), 1)
    fatigue = min(max(fatigue, 0), 1)
    attention = round(1 - fatigue, 2)

    # Round and return final state
    return {
        "stress": round(stress, 2),
        "fatigue": round(fatigue, 2),
        "attention": attention,
        "sensors": sensors
    }


# --- Demo execution ---
if __name__ == "__main__":
    print("🧠 Cognitive State Estimator Demo\n")
    for i in range(2):
        # Simulate random face and voice emotions
        face_emotion = random.choice(["happy", "neutral", "sad", "angry", "fear"])
        voice_emotion = random.choice(["calm", "neu", "angry", "sad", "happy"])
        state = estimate_cognitive_state(face_emotion, voice_emotion)

        print(f"[{i+1}] Face: {face_emotion:8} | Voice: {voice_emotion:7} → "
              f"Stress: {state['stress']:.2f} | Fatigue: {state['fatigue']:.2f} | "
              f"Attention: {state['attention']:.2f} | Sensors: {state['sensors']}")
        time.sleep(60)
