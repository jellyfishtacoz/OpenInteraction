import subprocess
import pyautogui

subprocess.run([r".venv\Scripts\python.exe", "eyetracking.py"])


pyautogui.moveTo(smoothed_x, smoothed_y)