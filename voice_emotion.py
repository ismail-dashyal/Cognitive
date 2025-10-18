import sounddevice as sd
from scipy.io.wavfile import write
import torch
import librosa
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification

def get_voice_emotion():
    samplerate = 16000
    duration = 5
    print("🎤 Recording 5s voice...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
    sd.wait()
    write("input.wav", samplerate, audio)

    model_name = "superb/wav2vec2-base-superb-er"
    processor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
    model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)

    y, sr = librosa.load("input.wav", sr=16000)
    inputs = processor(y, sampling_rate=16000, return_tensors="pt", padding=True)

    with torch.no_grad():
        logits = model(**inputs).logits
        pred = torch.argmax(logits, dim=-1)
    labels = model.config.id2label
    return labels[pred.item()]
