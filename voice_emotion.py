import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import torch
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification
import librosa

# -------- Step 1: Record audio --------
duration = 5  # seconds
fs = 16000
print("🎤 Recording ... Speak now for 5 seconds")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
sd.wait()
write("input.wav", fs, recording)
print("✅ Saved as input.wav")

# -------- Step 2: Load model and feature extractor --------
model_name = "superb/wav2vec2-base-superb-er"
extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)

# -------- Step 3: Load and preprocess audio --------
y, sr = librosa.load("input.wav", sr=16000)
inputs = extractor(y, sampling_rate=16000, return_tensors="pt", padding=True)

# -------- Step 4: Inference --------
with torch.no_grad():
    logits = model(**inputs).logits
pred = torch.argmax(logits, dim=-1)
label = model.config.id2label[pred.item()]
print(f"🧠 Predicted voice emotion/stress: {label}")

# --- Save voice emotion to shared file ---
import json
try:
    with open("realtime_data.json", "r") as f:
        existing = json.load(f)
except:
    existing = {}
existing["voice_emotion"] = label
with open("realtime_data.json", "w") as f:
    json.dump(existing, f)

