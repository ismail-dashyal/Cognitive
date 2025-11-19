# fusion_module.py
import random

def compute_cognitive_state(face_emotion, voice_emotion):
    """
    Estimate cognitive state (stress, fatigue, attention) 
    from REAL face and voice emotion inputs.
    """

    # Normalize inputs
    face = face_emotion.lower().strip() if face_emotion else "neutral"
    voice = voice_emotion.lower().strip() if voice_emotion else "neu"

    # Emotion → stress/fatigue mapping
    emotion_to_stress = {
        "angry": 0.9, "fear": 0.8, "sad": 0.7,
        "neutral": 0.4, "happy": 0.2, "surprise": 0.5,
        "calm": 0.2, "neu": 0.3, "hap": 0.3
    }

    emotion_to_fatigue = {
        "sad": 0.8, "neutral": 0.6, "angry": 0.5,
        "happy": 0.3, "fear": 0.6, "calm": 0.4, "surprise": 0.4,
        "neu": 0.5, "hap": 0.3
    }

    # Base values from emotions
    stress = (emotion_to_stress.get(face, 0.5) + emotion_to_stress.get(voice, 0.5)) / 2
    fatigue = (emotion_to_fatigue.get(face, 0.5) + emotion_to_fatigue.get(voice, 0.5)) / 2

    # Add light randomness to avoid flat behavior
    stress += random.uniform(-0.05, 0.05)
    fatigue += random.uniform(-0.05, 0.05)

    # Clamp
    stress = min(max(stress, 0), 1)
    fatigue = min(max(fatigue, 0), 1)

    # Attention inversely related
    attention = 1 - ((stress + fatigue) / 2)
    attention = min(max(attention, 0), 1)

    return {
        "stress": round(stress, 2),
        "fatigue": round(fatigue, 2),
        "attention": round(attention, 2)
    }


# Test mode
if __name__ == "__main__":
    for i in range(3):
        f = random.choice(["happy", "neutral", "sad", "angry", "fear", "calm"])
        v = random.choice(["hap", "neu", "sad", "angry", "calm"])
        print(f"Face={f}, Voice={v} → {compute_cognitive_state(f, v)}")
