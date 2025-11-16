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
            "head_x_input": "head_yaw",
            "eye_bthresh_h": 175,
            "eye_bthresh_v": 175,
            "head_bthresh_h": 0.1,
            "head_bthresh_v": 0.1,
            "head_mouse_range": 10,
            "eye_overlay_radius": 15,
            "show_overlay": True,
            "head_overlay_size": 100,
            "blink_is_click": False,
            "double_blink": True,
            "blink_keybind": "8",
            "button_up": "w",
            "button_down": "s",
            "button_left": "a",
            "button_right": "d",
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

def on_head_x_input_change(val):
    config["head_x_input"] = str(val)
    save_config()

def on_eye_bthresh_h_change(*args):
    val = eye_bthresh_h_var.get()
    config["eye_bthresh_h"] = float(val)
    save_config()

def on_eye_bthresh_v_change(*args):
    val = eye_bthresh_v_var.get()
    config["eye_bthresh_v"] = float(val)
    save_config()

def on_head_bthresh_h_change(*args):
    val = head_bthresh_h_var.get()
    config["head_bthresh_h"] = float(val)
    save_config()

def on_head_bthresh_v_change(*args):
    val = head_bthresh_v_var.get()
    config["head_bthresh_v"] = float(val)
    save_config()

def on_head_mouse_range_change(*args):
    val = head_mouse_range_var.get()
    config["head_mouse_range"] = float(val)
    save_config()

def on_eye_overlay_radius_change(*args):
    val = eye_overlay_radius_var.get()
    config["eye_overlay_radius"] = int(val)
    save_config()

def on_show_overlay_change(*args):
    config["show_overlay"] = show_overlay_var.get()
    save_config()

def on_button_up_change(*args):
    val = button_up_var.get()
    config["button_up"] = str(val)
    save_config()

def on_button_down_change(*args):
    val = button_down_var.get()
    config["button_down"] = str(val)
    save_config()

def on_button_left_change(*args):
    val = button_left_var.get()
    config["button_left"] = str(val)
    save_config()

def on_button_right_change(*args):
    val = button_right_var.get()
    config["button_right"] = str(val)
    save_config()

def on_head_overlay_size_change(*args):
    val = head_overlay_size_var.get()
    config["head_overlay_size"] = int(val)
    save_config()

updating_blink_flags = False

def on_blink_is_click_change(*args):
    global updating_blink_flags
    if updating_blink_flags:
        return  # avoid recursive calls

    val = blink_is_click_var.get()
    config["blink_is_click"] = val
    save_config()

    if val:  # it was turned ON
        updating_blink_flags = True
        blink_is_keybind_var.set(False)
        config["blink_is_keybind"] = False
        save_config()
        updating_blink_flags = False


def on_blink_is_keybind_change(*args):
    global updating_blink_flags
    if updating_blink_flags:
        return  # avoid recursive calls

    val = blink_is_keybind_var.get()
    config["blink_is_keybind"] = val
    save_config()

    if val:  # it was turned ON
        updating_blink_flags = True
        blink_is_click_var.set(False)
        config["blink_is_click"] = False
        save_config()
        updating_blink_flags = False

def on_double_blink_change(*args):
    config["double_blink"] = double_blink_var.get()
    save_config()

def on_blink_keybind_change(*args):
    val = blink_keybind_var.get()
    config["blink_keybind"] = str(val)
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

# ---------------- UI ----------------

root = tk.Tk()
root.title("openinteraction")
root.geometry("800x700")
root.bind("<Escape>", stop_process)

load_config()

# ---------- TOP CONTROLS ----------
top_frame = tk.Frame(root, pady=10)
top_frame.pack()

tk.Label(top_frame, text="Press for calibration").pack()
tk.Button(top_frame, text="Start Calibration", command=start_calibration).pack()

tk.Label(top_frame, text="Interface Control").pack(pady=(10, 0))

# Frame to hold Start and Stop buttons side by side
interface_frame = tk.Frame(top_frame)
interface_frame.pack(pady=5)

tk.Button(interface_frame, text="Start Interface", command=start_cursor).pack(side="left", padx=5)
tk.Button(interface_frame, text="Stop Interface", command=stop_process).pack(side="left", padx=5)


# ---------- SETTINGS FRAME ----------
settings = tk.Frame(root, padx=15, pady=15)
settings.pack(fill="x")

# Eye column
eye_frame = tk.Frame(settings)
eye_frame.grid(row=0, column=0, sticky="nw", padx=10)

def add_eye_row(label, widget):
    row = add_eye_row.row
    tk.Label(eye_frame, text=label).grid(row=row, column=0, sticky="w", pady=5)
    widget.grid(row=row, column=1, sticky="w", padx=10)
    add_eye_row.row += 1
add_eye_row.row = 0

tk.Label(eye_frame, text="Eye Control", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,10))
add_eye_row.row = 1  # start rows after header

# Head column
head_frame = tk.Frame(settings)
head_frame.grid(row=0, column=1, sticky="nw", padx=10)

def add_head_row(label, widget):
    row = add_head_row.row
    tk.Label(head_frame, text=label).grid(row=row, column=0, sticky="w", pady=5)
    widget.grid(row=row, column=1, sticky="w", padx=10)
    add_head_row.row += 1
add_head_row.row = 0

tk.Label(head_frame, text="Head Control", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,10))
add_head_row.row = 1  # start rows after header

# ---------- Add Eye Settings ----------
eye_options = ["move_cursor_eye", "press_key_eye", "off"]
eye_var = tk.StringVar(value=config.get("eye_action"))
eye_menu = tk.OptionMenu(eye_frame, eye_var, *eye_options, command=on_eye_actions_change)
add_eye_row("Eye Action", eye_menu)

eye_bthresh_h_var = tk.StringVar(value=config.get("eye_bthresh_h"))
eye_bthresh_h_var.trace_add("write", on_eye_bthresh_h_change)
add_eye_row("Eye Button Horizontal Threshold", tk.Entry(eye_frame, textvariable=eye_bthresh_h_var))

eye_bthresh_v_var = tk.StringVar(value=config.get("eye_bthresh_v"))
eye_bthresh_v_var.trace_add("write", on_eye_bthresh_v_change)
add_eye_row("Eye Button Vertical Threshold", tk.Entry(eye_frame, textvariable=eye_bthresh_v_var))

eye_overlay_radius_var = tk.StringVar(value=config.get("eye_overlay_radius"))
eye_overlay_radius_var.trace_add("write", on_eye_overlay_radius_change)
add_eye_row("Eye Overlay Radius", tk.Entry(eye_frame, textvariable=eye_overlay_radius_var))

blink_is_click_var = tk.BooleanVar(value=config["blink_is_click"])
blink_is_click_var.trace_add("write", on_blink_is_click_change)
add_eye_row("Blink is Click", tk.Checkbutton(eye_frame, variable=blink_is_click_var))

blink_is_keybind_var = tk.BooleanVar(value=config["blink_is_keybind"])
blink_is_keybind_var.trace_add("write", on_blink_is_keybind_change)
add_eye_row("Blink is Keybind", tk.Checkbutton(eye_frame, variable=blink_is_keybind_var))

double_blink_var = tk.BooleanVar(value=config["double_blink"])
double_blink_var.trace_add("write", on_double_blink_change)
add_eye_row("Double blink for blink Input", tk.Checkbutton(eye_frame, variable=double_blink_var))

blink_keybind_var = tk.StringVar(value=config.get("blink_keybind"))
blink_keybind_var.trace_add("write", on_blink_keybind_change)
add_eye_row("Blink Keybind", tk.Entry(eye_frame, textvariable=blink_keybind_var))

# ---------- Add Head Settings ----------
head_options = ["move_cursor_head", "press_key_head", "off"]
head_var = tk.StringVar(value=config.get("head_action"))
head_menu = tk.OptionMenu(head_frame, head_var, *head_options, command=on_head_actions_change)
add_head_row("Head Action", head_menu)

head_x_input_options = ["head_yaw", "head_tilt"]
head_x_input_var = tk.StringVar(value=config.get("head_x_input"))
head_x_input_menu = tk.OptionMenu(head_frame, head_x_input_var, *head_x_input_options, command=on_head_x_input_change)
add_head_row("Head X-Axis Input", head_x_input_menu)

head_bthresh_h_var = tk.StringVar(value=config.get("head_bthresh_h"))
head_bthresh_h_var.trace_add("write", on_head_bthresh_h_change)
add_head_row("Head Button Horizontal Threshold", tk.Entry(head_frame, textvariable=head_bthresh_h_var))

head_bthresh_v_var = tk.StringVar(value=config.get("head_bthresh_v"))
head_bthresh_v_var.trace_add("write", on_head_bthresh_v_change)
add_head_row("Head Button Vertical Threshold", tk.Entry(head_frame, textvariable=head_bthresh_v_var))

head_mouse_range_var = tk.StringVar(value=config.get("head_mouse_range"))
head_mouse_range_var.trace_add("write", on_head_mouse_range_change)
add_head_row("Head Mouse Range", tk.Entry(head_frame, textvariable=head_mouse_range_var))

head_overlay_size_var = tk.StringVar(value=config.get("head_overlay_size"))
head_overlay_size_var.trace_add("write", on_head_overlay_size_change)
add_head_row("Head Overlay Size", tk.Entry(head_frame, textvariable=head_overlay_size_var))


# ---------- BUTTON BINDINGS BELOW BOTH COLUMNS ----------
button_frame = tk.Frame(settings)
button_frame.grid(row=1, column=0, columnspan=2, pady=(20,0))  # span both columns

def add_button_row(label, widget):
    row = add_button_row.row
    tk.Label(button_frame, text=label).grid(row=row, column=0, sticky="w", pady=5)
    widget.grid(row=row, column=1, sticky="w", padx=10)
    add_button_row.row += 1
add_button_row.row = 0

tk.Label(button_frame, text="Other Settings", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,10))
add_button_row.row = 1

show_overlay_var = tk.BooleanVar(value=config["show_overlay"])
show_overlay_var.trace_add("write", on_show_overlay_change)
add_button_row("Show Overlay", tk.Checkbutton(button_frame, variable=show_overlay_var))

button_up_var = tk.StringVar(value=config.get("button_up"))
button_up_var.trace_add("write", on_button_up_change)
add_button_row("Up Button", tk.Entry(button_frame, textvariable=button_up_var))

button_down_var = tk.StringVar(value=config.get("button_down"))
button_down_var.trace_add("write", on_button_down_change)
add_button_row("Down Button", tk.Entry(button_frame, textvariable=button_down_var))

button_left_var = tk.StringVar(value=config.get("button_left"))
button_left_var.trace_add("write", on_button_left_change)
add_button_row("Left Button", tk.Entry(button_frame, textvariable=button_left_var))

button_right_var = tk.StringVar(value=config.get("button_right"))
button_right_var.trace_add("write", on_button_right_change)
add_button_row("Right Button", tk.Entry(button_frame, textvariable=button_right_var))


# ---------- FOOTER ----------
footer = tk.Frame(root, pady=10)
footer.pack(side="bottom", fill="x")

left = tk.Label(footer, text="Press ESC to exit")
left.pack(side="left", padx=20, anchor="w")

middle = tk.Label(footer, text="Press C to recenter")
middle.place(relx=0.5, rely=0.5, anchor="center")  # or use place to center precisely

right = tk.Label(footer, text="Press P to pause tracking")
right.pack(side="right", padx=20, anchor="e")

root.mainloop()