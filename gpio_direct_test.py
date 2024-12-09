#!/usr/bin/python3

import RPi.GPIO as GPIO
from signal import signal, SIGTERM, SIGHUP, pause
from time import sleep

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(32,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)

# blue?
GPIO.setup(40,GPIO.OUT)
GPIO.output(40, 0)

# GPIO.output(32, 0)
# GPIO.output(36, 0)
# GPIO.output(38, 0)
# GPIO.output(40, 0)

# sleep(3)

# GPIO.cleanup()

try:
        while (True):
                GPIO.output(38, 0)
                sleep(1)
                GPIO.output(36, 0)
                sleep(1)
                GPIO.output(32, 0)
                sleep(3)
                GPIO.output(32, 1)
                GPIO.output(36, 1)
                GPIO.output(38, 1)
                sleep(1)
except KeyboardInterrupt:
        pass
finally:
        GPIO.cleanup()