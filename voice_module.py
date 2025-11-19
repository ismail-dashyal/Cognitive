# voice_module.py

import sounddevice as sd
import torch
import librosa
from scipy.io.wavfile import write
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification

# --------------------------------------
# Load model once (fast + stable)
# --------------------------------------
MODEL_NAME = "superb/wav2vec2-base-superb-er"

try:
    extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
    model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()
except Exception as e:
    print("❌ Failed to load wav2vec model:", e)
    extractor = None
    model = None


def get_voice_emotion(duration=5):
    """
    Records audio for `duration` seconds, runs Wav2Vec2 emotion classification,
    returns label like: 'neu', 'hap', 'sad', 'ang', 'fea'.
    """

    # 1️⃣ Safety: Model loaded?
    if model is None or extractor is None:
        print("⚠️ Voice model unavailable — returning 'neu'")
        return "neu"

    fs = 16000
    print(f"🎤 Recording {duration}s voice...")
    
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
    except Exception as e:
        print("❌ Mic recording failed:", e)
        return "neu"

    # Save raw for debug
    write("input.wav", fs, recording)

    # 2️⃣ Load & preprocess audio safely
    try:
        y, sr = librosa.load("input.wav", sr=16000)
    except Exception as e:
        print("❌ Audio loading failed:", e)
        return "neu"

    # If audio is silent or tiny
    if len(y) < 2000:
        print("⚠️ Audio too short/silent")
        return "neu"

    # 3️⃣ Prepare features
    inputs = extractor(
        y,
        sampling_rate=16000,
        return_tensors="pt",
        padding=True
    )

    # 4️⃣ Inference
    with torch.no_grad():
        logits = model(**inputs).logits
        pred = torch.argmax(logits, dim=-1).item()

    emotion = model.config.id2label[pred]
    print("🗣️ Detected voice emotion:", emotion)

    return emotion


# Testing
if __name__ == "__main__":
    print("Detected:", get_voice_emotion())
