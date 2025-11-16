import pyautogui
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import time
import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()


def move_cursor_handler(x, y):
    pyautogui.moveTo(x, y)

# keypress ---
keyboard = KeyboardController()
pressed_keys = set()

SCREEN_W, SCREEN_H = pyautogui.size()

DIST_THRESHOLD = config["eye_bthresh"]  # distance on screen; used for left/right/up/down

LEFT_THRESHOLD = SCREEN_W / 2 - DIST_THRESHOLD
RIGHT_THRESHOLD = SCREEN_W / 2 + DIST_THRESHOLD
UP_THRESHOLD = SCREEN_H / 2 - DIST_THRESHOLD
DOWN_THRESHOLD = SCREEN_H / 2 + DIST_THRESHOLD

KEY_MAPPING = {
    "left": config["button_left"],
    "right": config["button_right"],
    "up": config["button_up"],
    "down": config["button_down"],
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
threshold = config["head_bthresh"]

def head_to_key_handler(rotd):
    global pressed_keys

    keys_to_press = set()

    xdif = rotd[0]
    ydif = rotd[1]

    # horizontal
    if xdif > threshold:
        keys_to_press.add(KEY_MAPPING["left"])
    elif xdif < -threshold:
        keys_to_press.add(KEY_MAPPING["right"])

    # vertical
    if ydif < -threshold:
        keys_to_press.add(KEY_MAPPING["up"])
    elif ydif > threshold:
        keys_to_press.add(KEY_MAPPING["down"])

    # Release keys that are no longer active
    for key in pressed_keys - keys_to_press:
        keyboard.release(key)
    # Press new keys
    for key in keys_to_press - pressed_keys:
        keyboard.press(key)

    pressed_keys = keys_to_press

# --- keypress from head
range = config["head_mouse_range"] * 0.1

def rotd_to_xy(rotd):
    rotd[0] / range
    x = SCREEN_W/2 + -(rotd[0] / range) * SCREEN_W/2
    y = SCREEN_H/2 + (rotd[1] / range) * SCREEN_H/2
    return x, y

def move_cursor_head_handler(rotd):
    x, y = rotd_to_xy(rotd)
    move_cursor_handler(x,y)