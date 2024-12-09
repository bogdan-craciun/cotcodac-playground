import os
from flask import Flask, send_file, render_template, abort
import RPi.GPIO as GPIO
from signal import signal, SIGTERM, SIGHUP, pause
from time import sleep

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<p>Hello, World!</p><a href="/blink">Blink</a>'

@app.route('/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = '/Users/bogdan'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('./files.html', files=files)

@app.route('/blink')
def blink():
  try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40,GPIO.OUT)
    GPIO.output(40, 0)
    sleep(3)
    GPIO.output(40, 1)
    GPIO.cleanup()
  except:
    pass
  finally:
    GPIO.cleanup()
