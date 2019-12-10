#!/usr/bin/env python

import sys
import time
import RPi.GPIO as gpio

# gpio setup
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
send = 20
test = 21
led_r = 25
led_g = 12
led_b = 16
buzzer = 5
gpio.setup(led_r, gpio.OUT, initial=gpio.LOW)
gpio.setup(led_g, gpio.OUT, initial=gpio.LOW)
gpio.setup(led_b, gpio.OUT, initial=gpio.LOW)

def discharge():
    gpio.setup(send, gpio.IN)
    gpio.setup(test, gpio.OUT)
    gpio.output(test, gpio.LOW)
    time.sleep(0.001)

def get_value(dt):
    result = dt * 100000
    result -= 5
    result = max(result, 0)
    result = min(result, 34)
    return result

def charge_time():
    gpio.setup(test, gpio.IN)
    gpio.setup(send, gpio.OUT)
    start = time.time()
    gpio.output(send, gpio.HIGH)
    while gpio.input(test) == gpio.LOW:
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
    gpio.cleanup()

sys.exit()
