import tkinter as tk
import subprocess

process = None  # global variable to store subprocess

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

# Calibration button
tk.Label(root, text="Press for calibration").pack(pady=20)
tk.Button(root, text="Start Calibration", command=start_calibration).pack()

# Cursor button
tk.Label(root, text="Press for cursor").pack(pady=20)
tk.Button(root, text="Start Cursor", command=start_cursor).pack()

# Bind Esc to stop subprocess
root.bind("<Escape>", stop_process)

root.mainloop()