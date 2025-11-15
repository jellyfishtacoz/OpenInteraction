import time
import os
import sys
import json

"""Simple JSON poller for `latest_gaze.json`.

Prints the file contents whenever it changes.
"""

DEFAULT_PATH = 'latest_gaze.json'


def poll_latest_json(path=DEFAULT_PATH, poll_interval=0.05):
    last_mtime = 0
    while True:
        try:
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                if mtime != last_mtime:
                    last_mtime = mtime
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            obj = json.load(f)
                        print(f"{obj.get('timestamp')} {obj.get('x')} {obj.get('y')}")
                    except Exception as e:
                        print('read error:', e)
            time.sleep(poll_interval)
        except KeyboardInterrupt:
            print('\nStopped')
            return


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    poll_latest_json(path)
