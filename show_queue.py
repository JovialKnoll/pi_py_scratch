#!/usr/bin/env python

import sys
import subprocess

import RPi.GPIO as gpio

#setup
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
data = 13
latch = 19
clock = 26
gpio.setup(data, gpio.OUT)
gpio.output(data, gpio.LOW)
gpio.setup(clock, gpio.OUT)
gpio.output(clock, gpio.LOW)
gpio.setup(latch, gpio.OUT)
gpio.output(latch, gpio.LOW)

def getIntArray(in_string):
    return [int(x) for x in in_string]

def getIOArray(in_string):
    return [gpio.LOW if i is 0 else gpio.HIGH for i in getIntArray(in_string)]

REVERSE = True

def setArray(in_string):
    right_string = in_string
    if REVERSE:
        right_string = reversed(in_string)
    gpio.output(latch, gpio.LOW)
    for i in getIOArray(right_string):
        gpio.output(data, i)
        gpio.output(clock, gpio.HIGH)
        gpio.output(clock, gpio.LOW)
        gpio.output(data, gpio.LOW) #clear
    gpio.output(latch, gpio.HIGH)

def setNumber(num):
    # 0 <= num <= 8
    s = ''.join(['1' for n in range(min(num, 8))])
    s += ''.join(['0' for n in range(8 - min(num, 8))])
    setArray(s)

command = 'lpstat -o HP_Deskjet_D1520 | wc -l'
response = subprocess.check_output(command, shell=True)
queue_length = int(response)
setNumber(queue_length)

gpio.cleanup()
sys.exit()
