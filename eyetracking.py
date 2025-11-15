import cv2
import pyautogui
from eyetrax import GazeEstimator

from overlay import Overlay
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
overlay = Overlay()
overlay.show()

estimator = GazeEstimator()
estimator.load_model("gaze_model.pkl")  # if you saved a model

# Get screen size for mapping
SCREEN_W, SCREEN_H = pyautogui.size()

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    features, blink = estimator.extract_features(frame)
    if features is not None and not blink:
        x, y = estimator.predict([features])[0]
        print(f"Gaze: ({x:.0f}, {y:.0f})")

        # KDE smoothing
        # smooth_x, smooth_y = kde_smooth_screen(history, sigma=10)

        # Move mouse
        pyautogui.moveTo(x, y)

        # update gaze position
        overlay.gaze_x = int(x)
        overlay.gaze_y = int(y)

    # Quit with 'q' -- doesnt work
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()