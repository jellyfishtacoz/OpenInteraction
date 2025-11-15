import pyautogui

def move_cursor_handler(x, y):
    """Moves the mouse to the gaze location"""
    pyautogui.moveTo(x, y)