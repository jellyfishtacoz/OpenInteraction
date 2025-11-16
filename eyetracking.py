import cv2
import pyautogui
from eyetrax import GazeEstimator
from overlay import *
from PyQt5.QtWidgets import QApplication
import sys
from eyetrax.filters import KDESmoother
from trackinghandlers import *
from pynput import keyboard
from calculateheadrot import get_head_rotation
import time
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()

eye_action = config["eye_action"]
head_action = config["head_action"]

eye_tracking = True
head_tracking = True

if eye_action == "off" and not config["blink_is_click"]: eye_tracking = False
if head_action == "off": head_tracking = False


def null(x, y): x = 0
handler_map = {
    "move_cursor_eye": move_cursor_handler,
    "move_cursor_head": move_cursor_head_handler,
    "press_key_eye": gaze_to_key_handler,
    "press_key_head": head_to_key_handler,
    "off": null,
}

active_eye_handler = handler_map[eye_action]
active_head_handler = handler_map[head_action]

app = QApplication(sys.argv)
c_overlay = CircleOverlay()
b_overlay = BoundaryOverlay()
h_overlay = HeadOverlay()

if config["show_overlay"]:
    if config["eye_action"] != "off": c_overlay.show()
    if eye_action == "press_key_eye": b_overlay.show()
    if head_action == "press_key_head": h_overlay.show()
estimator = GazeEstimator()
estimator.load_model("gaze_model.pkl")  # if you saved a model

SCREEN_W, SCREEN_H = pyautogui.size()
smoother = KDESmoother(SCREEN_W, SCREEN_H)

# toggle
enabled = True
rot = (0, 0, 0)
rot0 = (0, 0, 0)
rotd = (rot[0] - rot0[0], rot[1] - rot0[1], rot[2] - rot0[2])
calibrated = False

def on_press(key):
    global enabled
    global rot0
    try:
        if key.char == 'p':  # Press 'p' to pause
            enabled = not enabled
            print(f"Tracking enabled: {enabled}")
        if key.char == 'c':  # Press 't' to toggle
            rot0 = rot
            print(f"Recentered")
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

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
                rot = get_head_rotation(face, frame.shape[1], frame.shape[0])
                if not calibrated:
                    rot0 = rot
                    calibrated = True
                
                rotd = (rot[0] - rot0[0], rot[1] - rot0[1], rot[2] - rot0[2])
                print(rotd)

                active_head_handler(rotd)
                h_overlay.rotd = rotd

    if eye_tracking and enabled:
        features, blink = estimator.extract_features(frame)
        if features is not None and not blink:
            blink_state = False
            x, y = estimator.predict([features])[0]
            # print(f"Gaze: ({x:.0f}, {y:.0f})")

            smoothed_x, smoothed_y = smoother.step(x, y)  # feed to smoother

            # do action
            active_eye_handler(smoothed_x, smoothed_y)

            # update gaze position
            c_overlay.gaze_x = int(smoothed_x)
            c_overlay.gaze_y = int(smoothed_y)
                
        else:
            if not blink_state and config["blink_is_click"]:
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