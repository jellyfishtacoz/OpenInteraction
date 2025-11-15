import tkinter as tk
import subprocess

# Create window
root = tk.Tk()
root.title("openinteraction")
root.geometry("600x400")  # width x height

# Button
label = tk.Label(root, text="Press for calibration")
label.pack(pady=20)

def on_click():
    subprocess.run([r".venv\Scripts\python.exe", "calibrate.py"])

button = tk.Button(root, text="Click me", command=on_click)
button.pack()

# Button
label = tk.Label(root, text="Press for cursor")
label.pack(pady=20)

def on_click():
    subprocess.run([r".venv\Scripts\python.exe", "eyecursor.py"])

button = tk.Button(root, text="Click me", command=on_click)
button.pack()

# Run the app
root.mainloop()