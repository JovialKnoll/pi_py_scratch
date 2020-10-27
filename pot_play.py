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
READINGS_NUMBER = 16

GPIO.setup(LED_R, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_G, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_B, GPIO.OUT, initial=GPIO.LOW)

readings = deque([analog_read() for x in range(READINGS_NUMBER)], READINGS_NUMBER)
readings_sum = sum(readings)

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

def summed_read():
    readings_sum -= readings.popleft()
    readings.append(analog_read())
    readings_sum += readings[-1]
    # other processing here
    return readings_sum

def main():
    try:
        while True:
            print(summed_read())
            time.sleep(.1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

GPIO.cleanup()
sys.exit()
