from time import sleep
from signal import signal, SIGTERM, SIGHUP, pause

from rpi_lcd import LCD
from ina219 import INA219
from ina219 import DeviceRangeError

lcd = LCD()


def safe_exit(signum, frame):
    lcd.clear()
    exit(1)


signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.9


def doit():
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    ina.configure(ina.RANGE_16V)

    try:
        while True:
            sleep(1)
            print("Bus Voltage: %.3f V" % ina.voltage())
            print("Bus Current: %.3f mA" % ina.current())
            print("Power: %.3f mW" % ina.power())
            print("Shunt voltage: %.3f mV" % ina.shunt_voltage())

            lcd.text("%.3f V %.3f mA" % (ina.voltage(), ina.current()), 1)
            lcd.text(
                "%.3f mW %.3f mV" % (ina.power(), ina.shunt_voltage()),
                2,
            )
    except KeyboardInterrupt:
        lcd.clear()
        pass
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


if __name__ == "__main__":
    doit()
