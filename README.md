## OpenInteraction
Team 12 | Jack Dohrn, Bernie Dohrn

## Notes
- keybinds currently only work with letters and symbols
- eyetracking works best in well lit areas, close to the camera
- no current option to switch camera input, uses window's default

## Run Program
To run the program, simply run the file `openinteraction.py`

## Inspiration
OpenInteraction was inspired by the idea that computers should be accessible to everyone—especially people who cannot reliably use a mouse or keyboard. Commercial eye-tracking systems exist, but they are expensive, closed-source, and often difficult to customize.

We wanted to build a free, open, configurable interface that allows anyone to control their computer using just their eyes, head movements, or blinking. The goal was to create something lightweight, flexible, and customizable—something that could be adapted for gaming, accessibility, research, or general computer control.

## What it does
OpenInteraction turns a webcam into a full human-computer interaction system. It includes:

- **Eye tracking** using a machine-learning gaze model  
- **Head tracking** using MediaPipe 3D facial landmarks  
- **Customizable actions**, including cursor movement or mapping gaze/head direction to keyboard presses  
- **Blink detection** with optional double-blink clicking  
- **Live overlays** visualizing gaze, boundaries, and head motion  
- **Fully customizable settings**, including thresholds, actions, overlay sizes, and key bindings  
- **A GUI configuration tool** with real-time saving to JSON  
- **Hotkeys** for pause (P), recenter (C), and exit  
- **Calibration mode** to align the model to the user  

OpenInteraction functions as a standalone alternative to eye-tracking hardware, enabling hands-free control and accessibility interaction.

## How we built it
- **Python** for all core logic  
- **OpenCV** for camera capture  
- **MediaPipe Face Mesh** for head pose features  
- **Open Souce Gaze Estimation** (EyeTrax)  
- **KDE smoothing** to stabilize outputs  
- **PyQt5** for rendering overlays  
- **Tkinter** for the configuration GUI  
- **pynput** for keyboard simulation and hotkeys  
- **pyautogui** for cursor control  

The project is fully modular and uses handler maps to switch between cursor mode, keypress mode, or idle mode. Configuration is stored in `config.json` and updated live.

## Challenges we ran into
- Stabilizing the overlays without flicker  
- Mapping gaze coordinates to screen space  
- Smoothing movement without adding latency  
- Calibration drift in head tracking  
- Tkinter trace callbacks saving too aggressively  
- Preventing race conditions when saving config  
- Blink detection false positives in challenging lighting  
- Keeping eye and head control modes modular  
- Fixing overlays disappearing off-screen  

Building a system that combines ML, CV, GUI frameworks, and OS-level input required precise coordination.

## Accomplishments that we're proud of
- Complete eye- and head-tracking interface using only a webcam  
- Clean, real-time updating settings GUI  
- Reliable double-blink clicking  
- Three configurable overlays with live feedback  
- Highly customizable thresholds, keybindings, and overlay settings  
- Real-time smoothing for stable predictions  
- Enabling full hands-free PC control  

This project brings advanced accessibility functionality to anyone with a standard laptop camera.

## What we learned
- Integrating ML-based gaze tracking with CV-based head tracking  
- Building smoothing filters for noisy model output  
- Structuring multi-system real-time Python applications  
- Running Tkinter and PyQt without blocking each other  
- Importance of calibration and recenter hotkeys  
- Designing UI for accessibility-focused users  
- Creating modular handler maps  
- Robust blink detection across lighting/face variations  

## What's next for OpenInteraction
- More customizable gaze-to-key system  
- Additional keybind customizability  
- More overlay customization  
- Support for hardware eye-trackers  
- Gaming modes (e.g., joystick emulation)  
- YOLO-based player tracking in games  
- Multi-monitor support  
- Plugin system for custom actions  
- Integrated on-screen keyboard  
- Precision cursor mode  
- Standalone installer  
- Community-trained model improvements  
- Linux and macOS support  

The long-term goal is to evolve OpenInteraction into a fully open-source, customizable accessibility platform anyone can use and build upon.
