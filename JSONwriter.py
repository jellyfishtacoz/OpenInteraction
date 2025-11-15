import os
import time
import json

LATEST_JSON = "latest_gaze.json"
def write_latest_json(x, y, path=LATEST_JSON):
    """Atomically write the latest gaze position as JSON to `path`.

    Uses a '.tmp' file and `os.replace` to avoid partial reads by consumers.
    """
    tmp = path + '.tmp'
    try:
        payload = {"timestamp": time.time(), "x": int(x), "y": int(y)}
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(payload, f)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception as e:
        # don't raise; log and continue
        print("Error writing latest JSON gaze position:", e)