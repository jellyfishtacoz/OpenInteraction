import pyautogui
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time


def move_cursor_handler(x, y):
    """Moves the mouse to the gaze location"""
    pyautogui.moveTo(x, y)


# keypress ---
keyboard = KeyboardController()
pressed_keys = set()

SCREEN_W, SCREEN_H = pyautogui.size()

DIST_THRESHOLD = 175  # distance on screen; used for left/right/up/down

LEFT_THRESHOLD = SCREEN_W / 2 - DIST_THRESHOLD
RIGHT_THRESHOLD = SCREEN_W / 2 + DIST_THRESHOLD
UP_THRESHOLD = SCREEN_H / 2 - DIST_THRESHOLD
DOWN_THRESHOLD = SCREEN_H / 2 + DIST_THRESHOLD

KEY_MAPPING = {
    "left": 'a',
    "right": 'd',
    "up": 'w',
    "down": 's',
}

def gaze_to_key_handler(x, y):
    global pressed_keys

    keys_to_press = set()

    # horizontal
    if x < LEFT_THRESHOLD:
        keys_to_press.add(KEY_MAPPING["left"])
    elif x > RIGHT_THRESHOLD:
        keys_to_press.add(KEY_MAPPING["right"])

    # vertical
    if y < UP_THRESHOLD:
        keys_to_press.add(KEY_MAPPING["up"])
    elif y > DOWN_THRESHOLD:
        keys_to_press.add(KEY_MAPPING["down"])

    # Release keys that are no longer active
    for key in pressed_keys - keys_to_press:
        keyboard.release(key)
    # Press new keys
    for key in keys_to_press - pressed_keys:
        keyboard.press(key)

    pressed_keys = keys_to_press
    print(pressed_keys)

mouse = MouseController()

def blink_handler() :
    # Hold left button
    mouse.press(Button.left)

    time.sleep(0.2)  # hold for 200 ms

    # Release
    mouse.release(Button.left)

# --- keypress from head
threshold = 0.2

def head_to_key_handler(rot, rot0):
    global pressed_keys

    keys_to_press = set()

    # horizontal
    if (rot.x - rot0.x) > threshold:
        keys_to_press.add(KEY_MAPPING["left"])
    elif (rot.x - rot0.x) < threshold:
        keys_to_press.add(KEY_MAPPING["right"])

    # vertical
    if (rot.y - rot0.y) > threshold:
        keys_to_press.add(KEY_MAPPING["up"])
    elif (rot.y - rot0.y) < threshold:
        keys_to_press.add(KEY_MAPPING["down"])

    # Release keys that are no longer active
    for key in pressed_keys - keys_to_press:
        keyboard.release(key)
    # Press new keys
    for key in keys_to_press - pressed_keys:
        keyboard.press(key)

    pressed_keys = keys_to_press
    print(pressed_keys)