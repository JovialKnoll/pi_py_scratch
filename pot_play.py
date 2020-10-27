#!/usr/bin/env python

import sys
import time
import RPi.GPIO as gpio
from collections import deque

# gpio setup
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
send = 20
test = 21
led_r = 25
led_g = 12
led_b = 16
buzzer = 18
gpio.setup(led_r, gpio.OUT, initial=gpio.LOW)
gpio.setup(led_g, gpio.OUT, initial=gpio.LOW)
gpio.setup(led_b, gpio.OUT, initial=gpio.LOW)

readings_number = 16

def discharge():
    gpio.setup(send, gpio.IN)
    gpio.setup(test, gpio.OUT)
    gpio.output(test, gpio.LOW)
    time.sleep(0.001)

def charge_time():
    gpio.setup(test, gpio.IN)
    gpio.setup(send, gpio.OUT)
    start = time.time()
    gpio.output(send, gpio.HIGH)
    while gpio.input(test) == gpio.LOW:
        pass
    return time.time() - start

def analog_read():
    discharge()
    return charge_time()

def summed_read():
    readings_sum -= readings.popleft()
    readings.append(analog_read())
    readings_sum += readings[-1]
    # other processing here
    return readings_sum

def main():
    readings = deque([analog_read() for x in range(readings_number)], readings_number)
    readings_sum = sum(readings)

    try:
        while True:
            print(summed_read())
            time.sleep(.1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

gpio.cleanup()
sys.exit()
