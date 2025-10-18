from fer import FER
import cv2

def get_face_emotion():
    detector = FER(mtcnn=True)
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    if not ret:
        return "neutral"
    result = detector.detect_emotions(frame)
    if result:
        emotions = result[0]["emotions"]
        dominant = max(emotions, key=emotions.get)
        return dominant
    return "neutral"

if __name__ == "__main__":
    print(get_face_emotion())
