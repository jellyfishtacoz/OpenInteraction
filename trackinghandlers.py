import pyautogui
from pynput.keyboard import Controller, Key

def move_cursor_handler(x, y):
    """Moves the mouse to the gaze location"""
    pyautogui.moveTo(x, y)


# keypress ---
keyboard = Controller()
pressed_keys = set()

SCREEN_W, SCREEN_H = pyautogui.size()

EDGE_THRESHOLD = 0.4  # fraction of screen; used for left/right/up/down

LEFT_THRESHOLD = EDGE_THRESHOLD
RIGHT_THRESHOLD = 1 - EDGE_THRESHOLD
UP_THRESHOLD = EDGE_THRESHOLD
DOWN_THRESHOLD = 1 - EDGE_THRESHOLD

KEY_MAPPING = {
    "left": 'a',
    "right": 'd',
    "up": 'w',
    "down": 's',
}

def gaze_to_key_handler(x, y):
    global pressed_keys
    x_frac = x / SCREEN_W
    y_frac = y / SCREEN_H

    keys_to_press = set()

    # horizontal
    if x_frac < LEFT_THRESHOLD:
        keys_to_press.add(KEY_MAPPING["left"])
    elif x_frac > RIGHT_THRESHOLD:
        keys_to_press.add(KEY_MAPPING["right"])

    # vertical
    if y_frac < UP_THRESHOLD:
        keys_to_press.add(KEY_MAPPING["up"])
    elif y_frac > DOWN_THRESHOLD:
        keys_to_press.add(KEY_MAPPING["down"])

    # Release keys that are no longer active
    for key in pressed_keys - keys_to_press:
        keyboard.release(key)
    # Press new keys
    for key in keys_to_press - pressed_keys:
        keyboard.press(key)

    pressed_keys = keys_to_press
    print(pressed_keys)