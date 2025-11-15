from eyetrax import GazeEstimator, run_9_point_calibration

estimator = GazeEstimator()
run_9_point_calibration(estimator)

estimator.save_model("gaze_model.pkl")