import tkinter as tk
import subprocess
import json
import os

CONFIG_PATH = "config.json"
config = {}
process = None  # global variable to store subprocess

def load_config():
    global config
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    else:
        # default settings if no file exists
        config = {
            "eye_action": "move_cursor_eye",
            "head_action": "off",
            "eye_bthresh": 175,
            "head_bthresh": 0.02,
            "head_mouse_range": 1,
            "eye_overlay_radius": 15
        }
        save_config()

def save_config():
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    print("Config saved:", config)

def on_eye_actions_change(val):
    config["eye_action"] = str(val)
    save_config()

def on_head_actions_change(val):
    config["head_action"] = str(val)
    save_config()

def on_eye_bthresh_change(*args):
    val = eye_bthresh_var.get()
    config["eye_bthresh"] = float(val)
    save_config()

def on_head_bthresh_change(*args):
    val = head_bthresh_var.get()
    config["head_bthresh"] = float(val)
    save_config()

def on_head_mouse_range_change(*args):
    val = head_mouse_range_var.get()
    config["head_mouse_range"] = float(val)
    save_config()

def on_eye_overlay_radius_change(*args):
    val = eye_overlay_radius_var.get()
    config["eye_overlay_radius"] = int(val)
    save_config()

def start_calibration():
    global process
    if process is None or process.poll() is not None:  # not running
        process = subprocess.Popen([r".venv\Scripts\python.exe", "calibrate.py"])
    else:
        print("Calibration already running")

def start_cursor():
    global process
    if process is None or process.poll() is not None:
        process = subprocess.Popen([r".venv\Scripts\python.exe", "eyetracking.py"])
    else:
        print("Cursor tracking already running")

def stop_process(event=None):
    global process
    if process is not None and process.poll() is None:  # still running
        process.terminate()
        print("Process terminated")
        process = None

root = tk.Tk()
root.title("openinteraction")
root.geometry("600x400")

root.bind("<Escape>", stop_process)

load_config()

# Calibration button
tk.Label(root, text="Press for calibration").pack(pady=(20,0))
tk.Button(root, text="Start Calibration", command=start_calibration).pack()

# Cursor button
tk.Label(root, text="Press for cursor").pack(pady=(10,0))
tk.Button(root, text="Start Cursor", command=start_cursor).pack()

# Bind Esc to stop subprocess
root.bind("<Escape>", stop_process)

# Settings UI
tk.Label(root, text="Eye Action").pack(pady=(20,0))
eye_options = ["move_cursor_eye", "press_key_eye", "off"]
eye_var = tk.StringVar(value=config.get("eye_action"))
eye_menu = tk.OptionMenu(root, eye_var, *eye_options, command=on_eye_actions_change)
eye_menu.pack()

tk.Label(root, text="Head Action").pack(pady=(10,0))
head_options = ["move_cursor_head", "press_key_head", "off"]
head_var = tk.StringVar(value=config.get("head_action"))
head_menu = tk.OptionMenu(root, head_var, *head_options, command=on_head_actions_change)
head_menu.pack()

tk.Label(root, text="Eye Button Threshold").pack(pady=(10,0))
eye_bthresh_var = tk.StringVar(value=config.get("eye_bthresh"))
eye_bthresh_var.trace_add("write", on_eye_bthresh_change)
eye_bthresh_entry = tk.Entry(root, textvariable=eye_bthresh_var)
eye_bthresh_entry.pack(pady=5)

tk.Label(root, text="Head Button Threshold").pack(pady=(10,0))
head_bthresh_var = tk.StringVar(value=config.get("head_bthresh"))
head_bthresh_var.trace_add("write", on_head_bthresh_change)
head_bthresh_entry = tk.Entry(root, textvariable=head_bthresh_var)
head_bthresh_entry.pack()

tk.Label(root, text="Head Mouse Range").pack(pady=(10,0))
head_mouse_range_var = tk.StringVar(value=config.get("head_mouse_range"))
head_mouse_range_var.trace_add("write", on_head_mouse_range_change)
head_mouse_range_entry = tk.Entry(root, textvariable=head_mouse_range_var)
head_mouse_range_entry.pack()

tk.Label(root, text="Eye Overlay Radius").pack(pady=(10,0))
eye_overlay_radius_var = tk.StringVar(value=config.get("eye_overlay_radius"))
eye_overlay_radius_var.trace_add("write", on_eye_overlay_radius_change)
eye_overlay_radius_entry = tk.Entry(root, textvariable=eye_overlay_radius_var)
eye_overlay_radius_entry.pack()

root.mainloop()