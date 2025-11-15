import cv2
import pyautogui
from eyetrax import GazeEstimator
from overlay import Overlay
from PyQt5.QtWidgets import QApplication
import sys
from eyetrax.filters import KDESmoother
from trackinghandlers import move_cursor_handler, gaze_to_key_handler
from pynput import keyboard

settings = ["move_cursor"]  # could be loaded from a config
eye_tracking = False
head_tracking = True

handler_map = {
    "move_cursor": move_cursor_handler,
    "press_key": gaze_to_key_handler,
}

app = QApplication(sys.argv)
overlay = Overlay()
if eye_tracking: overlay.show()

estimator = GazeEstimator()
estimator.load_model("gaze_model.pkl")  # if you saved a model

SCREEN_W, SCREEN_H = pyautogui.size()
smoother = KDESmoother(SCREEN_W, SCREEN_H)

# toggle
enabled = True

def on_press(key):
    global enabled
    try:
        if key.char == 't':  # Press 't' to toggle
            enabled = not enabled
            print(f"Eye tracking enabled: {enabled}")
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

active_handlers = [handler_map[s] for s in settings]

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    if head_tracking:
        face_mesh = estimator.face_mesh
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            for face in results.multi_face_landmarks:
                # Extract 3D landmarks for head pose estimation
                if enabled:
                    print(face.landmark[0].x, face.landmark[0].y, face.landmark[0].z)

    if eye_tracking:
        features, blink = estimator.extract_features(frame)
        if features is not None and not blink:
            x, y = estimator.predict([features])[0]
            # print(f"Gaze: ({x:.0f}, {y:.0f})")

            smoothed_x, smoothed_y = smoother.step(x, y)  # feed to smoother

            # do action
            if enabled:
                for handler in active_handlers:
                    handler(smoothed_x, smoothed_y)

            # update gaze position
            overlay.gaze_x = int(smoothed_x)
            overlay.gaze_y = int(smoothed_y)

    # Quit with 'q' -- doesnt work
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()