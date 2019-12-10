#!/usr/bin/env python

import sys
import time
import RPi.GPIO as gpio

# gpio setup
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
led_r = 25
led_g = 12
led_b = 16
buzzer = 18
gpio.setup(led_r, gpio.OUT, initial=gpio.LOW)
gpio.setup(led_g, gpio.OUT, initial=gpio.LOW)
gpio.setup(led_b, gpio.OUT, initial=gpio.LOW)
gpio.setup(buzzer, gpio.OUT)
pulse = gpio.PWM(buzzer, .5)
duty = 20

try:
    pulse.start(duty)
    gpio.output(led_r, gpio.HIGH)
    gpio.output(led_g, gpio.HIGH)
    time.sleep(.5)
    pulse.ChangeFrequency(80)
    gpio.output(led_r, gpio.LOW)
    gpio.output(led_b, gpio.HIGH)
    time.sleep(.5)
    pulse.ChangeFrequency(100)
    gpio.output(led_r, gpio.HIGH)
    gpio.output(led_g, gpio.LOW)
    time.sleep(.5)
    pulse.ChangeFrequency(120)
    gpio.output(led_g, gpio.HIGH)
    time.sleep(.5)
except KeyboardInterrupt:
    pass
finally:
    pulse.stop()
    gpio.cleanup()

sys.exit()
