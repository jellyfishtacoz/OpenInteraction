import tkinter as tk

# Create window
root = tk.Tk()
root.title("openinteraction")
root.geometry("600x400")  # width x height

# Add a label
label = tk.Label(root, text="Press for eyetracking")
label.pack(pady=20)

# Add a button
def on_click():
    label.config(text="Button clicked!")

button = tk.Button(root, text="Click me", command=on_click)
button.pack()

# Run the app
root.mainloop()