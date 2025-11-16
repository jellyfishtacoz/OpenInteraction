import math

def get_head_rotation(face, w, h):
    """
    Returns (pitch, yaw, roll) in degrees 
    using MediaPipe FaceMesh landmarks.
    """

    # Key landmarks
    NOSE = 1
    LEFT_EYE = 33
    RIGHT_EYE = 263
    CHIN = 152

    # Convert to pixel coordinates
    nose = face.landmark[NOSE]
    leye = face.landmark[LEFT_EYE]
    reye = face.landmark[RIGHT_EYE]
    chin = face.landmark[CHIN]

    p_nose = (nose.x * w, nose.y * h)
    p_leye = (leye.x * w, leye.y * h)
    p_reye = (reye.x * w, reye.y * h)
    p_chin = (chin.x * w, chin.y * h)

    # --- YAW (turn left/right) ---
    # How far the nose is left/right relative to eyes
    eye_mid_x = (p_leye[0] + p_reye[0]) / 2
    yaw = math.degrees(math.atan2(p_nose[0] - eye_mid_x,
                                  abs(p_reye[0] - p_leye[0])))

    # --- ROLL (tilt head sideways) ---
    eye_dx = p_reye[0] - p_leye[0]
    eye_dy = p_reye[1] - p_leye[1]
    roll = math.degrees(math.atan2(eye_dy, eye_dx))

    # --- PITCH (look up/down) ---
    eye_mid_y = (p_leye[1] + p_reye[1]) / 2
    pitch = math.degrees(math.atan2(eye_mid_y - p_nose[1],
                                    abs(p_reye[0] - p_leye[0])))

    return yaw, pitch, roll
