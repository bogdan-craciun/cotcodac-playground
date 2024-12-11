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
    exit(1)


signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

if len(sys.argv) != 2:
    print("Usage: display_test.py '{line1: str, line2: str}'")
    print("Maximum 16 characters per line")
    sys.exit(1)

json_data = sys.argv[1]
data = json.loads(json_data)

print(data["line1"])
print(data["line2"])

# line1 = sys.argv[1][:16]
# line2 = sys.argv[2][:16]

try:
    lcd.text(line1, 1)
    lcd.text(line2, 2)
    sleep(3)
    # pause()
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
