import cv2
import pyautogui
from eyetrax import GazeEstimator
from JSONwriter import write_latest_json
from overlay import Overlay
from PyQt5.QtWidgets import QApplication
import sys
from eyetrax.filters import KDESmoother

app = QApplication(sys.argv)
overlay = Overlay()
overlay.show()

estimator = GazeEstimator()
estimator.load_model("gaze_model.pkl")  # if you saved a model

SCREEN_W, SCREEN_H = pyautogui.size()
smoother = KDESmoother(SCREEN_W, SCREEN_H)
smoother.tune(estimator, camera_index=0)

# Latest single-file JSON for consumers (atomic writes)
LATEST_JSON = "latest_gaze.json"

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    features, blink = estimator.extract_features(frame)
    if features is not None and not blink:
        x, y = estimator.predict([features])[0]
        print(f"Gaze: ({x:.0f}, {y:.0f})")

        smoothed_x, smoothed_y = smoother.step(x, y)  # feed to smoother

        #Send coords to JSON:
        write_latest_json(x, y, LATEST_JSON)

        # update gaze position
        overlay.gaze_x = int(smoothed_x)
        overlay.gaze_y = int(smoothed_y)

    # Quit with 'q' -- doesnt work
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()