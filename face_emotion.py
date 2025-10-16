import cv2, json, time
from fer import FER

detector = FER(mtcnn=True)
cam = cv2.VideoCapture(0)

print("🎥 Real-time Face Emotion Detection Started... Press Q to quit")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    results = detector.detect_emotions(frame)

    if results:
        emotions = results[0]["emotions"]
        top_emotion = max(emotions, key=emotions.get)

        # Save emotion to shared file
        data = {"face_emotion": top_emotion}
        try:
            with open("realtime_data.json", "r") as f:
                existing = json.load(f)
        except:
            existing = {}
        existing.update(data)
        with open("realtime_data.json", "w") as f:
            json.dump(existing, f)

        # Display emotion on screen
        cv2.putText(frame, top_emotion, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Face Emotion (Press Q to quit)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print("🛑 Face emotion detection stopped.")
