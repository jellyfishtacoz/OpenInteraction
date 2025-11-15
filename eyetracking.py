import cv2
import pyautogui
from eyetrax import GazeEstimator
from overlay import Overlay
from PyQt5.QtWidgets import QApplication
import sys
from eyetrax.filters import KDESmoother
from trackinghandlers import move_cursor_handler, gaze_to_key_handler, blink_handler
from pynput import keyboard
import time

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

# blink data
last_blink_time = 0
blink_count = 0
double_blink_threshold = 0.5  # seconds
blink_state = False

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
            # x, y = estimator.predict([features])[0]
            x, y = (100,100)
            # print(f"Gaze: ({x:.0f}, {y:.0f})")
    features, blink = estimator.extract_features(frame)
    if features is not None and not blink:
        blink_state = False
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
        # update gaze position
        overlay.gaze_x = int(smoothed_x)
        overlay.gaze_y = int(smoothed_y)
    else :
        if not blink_state :
            # Blink detected
            blink_state = True
            current_time = time.time()
            if current_time - last_blink_time < double_blink_threshold:
                blink_count += 1
            else:
                blink_count = 1  # reset count if too long

            last_blink_time = current_time

            if blink_count == 2:
                print("Double blink detected! Clicking mouse...")
                blink_handler()
                blink_count = 0  # reset after double blink

    # Quit with 'q' -- doesnt work
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()