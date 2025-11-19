# face_module.py
import cv2
import traceback
from fer import FER

# Initialize detector once (expensive operation)
try:
    detector = FER(mtcnn=True)
except Exception as e:
    detector = None
    print("⚠️ Warning: FER detector failed to initialize:", e)

def _detect_frame_emotion(frame):
    """Return dominant emotion label for a single BGR frame, or 'neutral' on failure."""
    global detector
    if detector is None:
        # Try lazy initialization (best-effort)
        try:
            detector = FER(mtcnn=True)
        except Exception as e:
            print("⚠️ FER initialization failed inside detection:", e)
            return "neutral"

    try:
        results = detector.detect_emotions(frame)
        if not results:
            return "neutral"
        emotions = results[0].get("emotions", {})
        if not emotions:
            return "neutral"
        return max(emotions, key=emotions.get)
    except Exception:
        # detection failed for some reason
        traceback.print_exc()
        return "neutral"

def get_face_emotion(device_index=0, read_timeout=2):
    """
    Capture a single frame from webcam and return dominant face emotion.
    - device_index: which camera (0 default)
    - read_timeout: seconds to wait for a frame
    Returns a string emotion label (e.g., 'happy', 'neutral', 'angry') or 'neutral' on error.
    """
    try:
        cam = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)  # use CAP_DSHOW on Windows to reduce warnings
    except Exception:
        cam = cv2.VideoCapture(device_index)

    if not cam or not cam.isOpened():
        print("⚠️ Webcam not available or couldn't be opened.")
        return "neutral"

    # try to read a frame for up to read_timeout seconds
    start = cv2.getTickCount()
    fps = cam.get(cv2.CAP_PROP_FPS) or 30.0
    frame = None
    end_time = cv2.getTickCount() + read_timeout * cv2.getTickFrequency()
    while cv2.getTickCount() < end_time:
        ret, frm = cam.read()
        if ret and frm is not None:
            frame = frm
            break

    cam.release()

    if frame is None:
        print("⚠️ Failed to read frame from webcam within timeout.")
        return "neutral"

    return _detect_frame_emotion(frame)


# Backwards-compatible alias used by some versions of app.py
def capture_face_emotion(*args, **kwargs):
    return get_face_emotion(*args, **kwargs)


# Quick test when running this file directly
if __name__ == "__main__":
    print("Testing face capture...")
    em = get_face_emotion()
    print("Detected face emotion:", em)
