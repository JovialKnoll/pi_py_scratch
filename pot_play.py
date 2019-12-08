import sys
import time
import RPi.GPIO as GPIO

set = 20
test = 21

led_r = 25
led_g = 12
led_b = 16
buzzer = 5

GPIO.setmode(GPIO.BCM)

def discharge():
    GPIO.setup(set, GPIO.IN)
    GPIO.setup(test, GPIO.OUT)
    GPIO.output(test, False)
    time.sleep(0.001)

def get_value(dt):
    result = dt * 100000
    result -= 5
    return result

def charge_time():
    GPIO.setup(test, GPIO.IN)
    GPIO.setup(set, GPIO.OUT)
    start = time.time()
    GPIO.output(set, True)
    while not GPIO.input(test):
        pass
    return get_value(time.time() - start)

def analog_read():
    discharge()
    return charge_time()

try:
    while True:
        print(analog_read())
        time.sleep(.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

sys.exit()
