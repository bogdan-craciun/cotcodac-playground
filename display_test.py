#!/usr/bin/python3

from signal import signal, SIGTERM, SIGHUP, pause
import sys
sys.path.insert(0, '/home/bogdan/my-venv/lib/python3.11/site-packages')
from rpi_lcd import LCD

lcd = LCD()

def safe_exit(signum, frame):
  exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
  lcd.text("Ce faci", 1)
  lcd.text("Sweetie?", 2)
  pause()
except KeyboardInterrupt:
  pass
finally:
  lcd.clear()
