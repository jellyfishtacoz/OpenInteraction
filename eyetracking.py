import cv2
from eyetrax import GazeEstimator

estimator = GazeEstimator()
estimator.load_model("gaze_model.pkl")  # if you saved a model

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    features, blink = estimator.extract_features(frame)
    if features is not None and not blink:
        x, y = estimator.predict([features])[0]
        print(f"Gaze: ({x:.0f}, {y:.0f})")
