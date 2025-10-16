import sounddevice as sd, torch, librosa, json
from scipy.io.wavfile import write
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification

def get_voice_emotion(duration=5):
    fs = 16000
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    write("input.wav", fs, recording)

    model_name = "superb/wav2vec2-base-superb-er"
    extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
    model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)

    y, sr = librosa.load("input.wav", sr=16000)
    inputs = extractor(y, sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    pred = torch.argmax(logits, dim=-1)
    return model.config.id2label[pred.item()]

if __name__ == "__main__":
    print("Detected voice emotion:", get_voice_emotion())
