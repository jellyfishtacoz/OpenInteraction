import cv2
import pyautogui
from eyetrax import GazeEstimator

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer
import sys

estimator = GazeEstimator()
estimator.load_model("gaze_model.pkl")  # if you saved a model

# Get screen size for mapping
SCREEN_W, SCREEN_H = pyautogui.size()

# Overlay
class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1920, 1080)
        self.gaze_x = 960
        self.gaze_y = 540

        # refresh every 30ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(255, 0, 0, 150)))  # semi-transparent red
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.gaze_x-15, self.gaze_y-15, 30, 30)

app = QApplication(sys.argv)
overlay = Overlay()
overlay.show()

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    features, blink = estimator.extract_features(frame)
    if features is not None and not blink:
        x, y = estimator.predict([features])[0]
        print(f"Gaze: ({x:.0f}, {y:.0f})")

    # move mouse
    pyautogui.moveTo(x, y)

    # update gaze position
    overlay.gaze_x = int(x)
    overlay.gaze_y = int(y)

    # Quit with 'q' -- doesnt work
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()