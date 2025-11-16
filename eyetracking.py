import cv2
import pyautogui
from eyetrax import GazeEstimator
from overlay import CircleOverlay, BoundaryOverlay
from PyQt5.QtWidgets import QApplication
import sys
from eyetrax.filters import KDESmoother
from trackinghandlers import move_cursor_handler, gaze_to_key_handler, blink_handler, head_to_key_handler
from pynput import keyboard
import time
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()

eye_actions = [config["eye_actions"]]  # could be loaded from a config
head_actions = [config["head_actions"]]
eye_tracking = True
head_tracking = True

handler_map = {
    "move_cursor": move_cursor_handler,
    "press_key_eye": gaze_to_key_handler,
    "press_key_head": head_to_key_handler,
}

app = QApplication(sys.argv)
c_overlay = CircleOverlay()
b_overlay = BoundaryOverlay(175)
c_overlay.hide()
b_overlay.hide()

if eye_tracking:
    c_overlay.show()

if head_tracking:
    if "press_key_eye" in eye_actions:
        b_overlay.show()

estimator = GazeEstimator()
estimator.load_model("gaze_model.pkl")  # if you saved a model

SCREEN_W, SCREEN_H = pyautogui.size()
smoother = KDESmoother(SCREEN_W, SCREEN_H)

# toggle
enabled = True
rot = (0, 0, 0)
rot0 = (0, 0, 0)
rotd = (rot[0] - rot0[0], rot[1] - rot0[1], rot[2] - rot0[2])

def on_press(key):
    global enabled
    global rot0
    try:
        if key.char == 't':  # Press 't' to toggle
            enabled = not enabled
            print(f"Tracking enabled: {enabled}")
        if key.char == 'c':  # Press 't' to toggle
            rot0 = rot
            print(f"Recentered")
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

active_eye_handlers = [handler_map[s] for s in eye_actions]
active_head_handlers = [handler_map[s] for s in head_actions]

# blink data
last_blink_time = 0
blink_count = 0
double_blink_threshold = 0.5  # seconds
blink_state = False

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    if head_tracking and enabled:
        face_mesh = estimator.face_mesh
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            for face in results.multi_face_landmarks:
                # Extract 3D landmarks for head pose estimation
                rot = (face.landmark[0].x, face.landmark[0].y, face.landmark[0].z)
                rotd = (rot[0] - rot0[0], rot[1] - rot0[1], rot[2] - rot0[2])

                for handler in active_head_handlers:
                    handler(rotd)

    if eye_tracking and enabled:
        features, blink = estimator.extract_features(frame)
        if features is not None and not blink:
            blink_state = False
            x, y = estimator.predict([features])[0]
            # print(f"Gaze: ({x:.0f}, {y:.0f})")

            smoothed_x, smoothed_y = smoother.step(x, y)  # feed to smoother

            # do action
            for handler in active_eye_handlers:
                handler(smoothed_x, smoothed_y)

            # update gaze position
            c_overlay.gaze_x = int(smoothed_x)
            c_overlay.gaze_y = int(smoothed_y)
                
        else:
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