import os
import time
import json

LATEST_JSON = "latest_gaze.json"
def write_latest_json(x, y, blink, path=LATEST_JSON):
    """Atomically write the latest gaze position as JSON to `path`.

    Uses a '.tmp' file and `os.replace` to avoid partial reads by consumers.
    """
    tmp = path + '.tmp'
    try:
        payload = {"timestamp": time.time(), "x": int(x), "y": int(y), "blink": bool(blink)}
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(payload, f)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception as e:
        # don't raise; log and continue
        print("Error writing latest JSON gaze position:", e)

def poll_latest_json(path=LATEST_JSON):
    last_mtime = 0
    try:
        if os.path.exists(path):
            mtime = os.path.getmtime(path)
            if mtime != last_mtime:
                last_mtime = mtime
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        obj = json.load(f)
                    return obj.get('x'), obj.get('y'), obj.get('blink')
                except Exception as e:
                    print('read error:', e)
    except KeyboardInterrupt:
        print('\nStopped')
        return