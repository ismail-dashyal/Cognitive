import cv2, json
from fer import FER

def get_face_emotion():
    cam = cv2.VideoCapture(0)
    detector = FER(mtcnn=True)
    ret, frame = cam.read()
    cam.release()
    if not ret:
        return "neutral"

    result = detector.detect_emotions(frame)
    if not result:
        return "neutral"

    emotions = result[0]["emotions"]
    top = max(emotions, key=emotions.get)
    return top

if __name__ == "__main__":
    emotion = get_face_emotion()
    print("Detected face emotion:", emotion)
