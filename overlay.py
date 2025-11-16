# overlay.py
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QTimer
import pyautogui
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()

SCREEN_W, SCREEN_H = pyautogui.size()
OVERLAY_RADIUS = config["eye_overlay_radius"]

class CircleOverlay(QWidget):
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
        painter.drawEllipse(self.gaze_x-OVERLAY_RADIUS, self.gaze_y-OVERLAY_RADIUS, OVERLAY_RADIUS*2, OVERLAY_RADIUS*2)

class BoundaryOverlay(QWidget):
    def __init__(self, threshold):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        # transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.screen_w = QApplication.primaryScreen().size().width()
        self.screen_h = QApplication.primaryScreen().size().height()

        self.threshold = threshold

        self.setGeometry(0, 0, self.screen_w, self.screen_h)
        self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor(0, 255, 0, 180), 3)
        p.setPen(pen)

        # vertical boundaries
        x1 = int(self.screen_w / 2 - self.threshold)
        x2 = int(self.screen_w / 2 + self.threshold)

        # horizontal boundaries
        y1 = int(self.screen_h / 2 - self.threshold)
        y2 = int(self.screen_h / 2 + self.threshold)

        # draw lines
        p.drawLine(x1, 0, x1, self.screen_h)
        p.drawLine(x2, 0, x2, self.screen_h)

        p.drawLine(0, y1, self.screen_w, y1)
        p.drawLine(0, y2, self.screen_w, y2)