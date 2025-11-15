# overlay.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer
import pyautogui

SCREEN_W, SCREEN_H = pyautogui.size()
OVERLAY_RADIUS = 15

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
        painter.drawEllipse(self.gaze_x-OVERLAY_RADIUS, self.gaze_y-OVERLAY_RADIUS, OVERLAY_RADIUS*2, OVERLAY_RADIUS*2)