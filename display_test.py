#!.venv/bin/python3

# Or, use this if system-wide: #!/usr/bin/python3

import sys
import json
from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause

from rpi_lcd import LCD

# sys.path.insert(0, "/home/bogdan/my-venv/lib/python3.11/site-packages")

lcd = LCD()


def safe_exit(signum, frame):
    lcd.clear()
    exit(1)


signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

if len(sys.argv) != 2:
    print("Usage: display_test.py '{line1: str, line2: str}'")
    print("Maximum 16 characters per line")
    sys.exit(1)

json_data = sys.argv[1]
data = json.loads(json_data)
line1 = ""
line2 = ""

if "line1" in data:
    line1 = data["line1"][:16]
if "line2" in data:
    line2 = data["line2"][:16]

try:
    lcd.text(line1, 1)
    lcd.text(line2, 2)
    # sleep(3)
    # pause()
except Exception as e:
    print(e)
    safe_exit()
except KeyboardInterrupt:
    pass
# finally:
# lcd.clear()
