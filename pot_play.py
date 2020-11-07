#!/usr/bin/env python

import sys
import time
import RPi.GPIO as GPIO
from collections import deque

# gpio setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
SEND = 20
TEST = 21
LED_R = 25
LED_G = 12
LED_B = 16
BUZZER = 18
READINGS_NUMBER = 8
MAX_LEVEL = 7
LARGEST_SUM = 0.0031
SMALLEST_SUM = 0.0005

GPIO.setup(LED_R, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_G, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_B, GPIO.OUT, initial=GPIO.LOW)

def discharge():
    GPIO.setup(SEND, GPIO.IN)
    GPIO.setup(TEST, GPIO.OUT)
    GPIO.output(TEST, GPIO.LOW)
    time.sleep(0.001)

def charge_time():
    GPIO.setup(TEST, GPIO.IN)
    GPIO.setup(SEND, GPIO.OUT)
    start = time.time()
    GPIO.output(SEND, GPIO.HIGH)
    while GPIO.input(TEST) == GPIO.LOW:
        pass
    return time.time() - start

def analog_read():
    discharge()
    return charge_time()

def get_level(summed_read):
    return min(
        max(summed_read - SMALLEST_SUM, 0) * (MAX_LEVEL + 1) / (LARGEST_SUM - SMALLEST_SUM),
        MAX_LEVEL
    )

readings = deque([analog_read() for x in range(READINGS_NUMBER)], READINGS_NUMBER)
readings_sum = sum(readings)

def summed_read():
    global readings, readings_sum
    readings_sum -= readings.popleft()
    readings.append(analog_read())
    readings_sum += readings[-1]
    # other processing here
    # get a number from 0-7?
    return readings_sum

#OFF
#RED
#RED GREEN
#GREEN
#GREEN BLUE
#BLUE
#RED BLUE
#RED GREEN BLUE / pulse

def main():
    try:
        while True:
            level = get_level(summed_read())
            print(level)
            time.sleep(.1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

GPIO.cleanup()
sys.exit()
