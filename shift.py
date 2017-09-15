import sys, time
import RPi.GPIO as gpio

REVERSE = False

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

single_led = 21
gpio.setup(single_led, gpio.OUT)

REVERSE = True

def blinkSingle():
    gpio.output(single_led, gpio.HIGH)
    time.sleep(1)
    gpio.output(single_led, gpio.LOW)
    time.sleep(1)
#for i in range(3):
#    blinkSingle()

data = 13
latch = 19
clock = 26
small_time = 0#0.0001

gpio.setup(data, gpio.OUT)
gpio.output(data, gpio.LOW)

gpio.setup(clock, gpio.OUT)
gpio.output(clock, gpio.LOW)

gpio.setup(latch, gpio.OUT)
gpio.output(latch, gpio.LOW)

def getIntArray(in_string):
    return [int(x) for x in in_string]
def setArray(in_string):
    right_string = in_string
    if REVERSE:
        right_string = reversed(in_string)
    gpio.output(latch, gpio.LOW)
    for i in getIntArray(right_string):
        if i is 0:
            gpio.output(data, gpio.LOW)
        else:
            gpio.output(data, gpio.HIGH)
        time.sleep(small_time)
        gpio.output(clock, gpio.HIGH)
        time.sleep(small_time)
        gpio.output(clock, gpio.LOW)
        gpio.output(data, gpio.LOW)#clear
    gpio.output(latch, gpio.HIGH)
def setNumber(num):
    # 0 <= num <= 8
    s = ''.join(['1' for n in range(num)])
    s += ''.join(['0' for n in range(8 - num)])
    setArray(s)

slow_time = 0.5
quick_time = 0.1
setArray('10000000')
time.sleep(slow_time)
setArray('11000000')
time.sleep(slow_time)
setArray('11100000')
time.sleep(slow_time)
setArray('00000000')
time.sleep(slow_time)
setArray('10000001')
time.sleep(slow_time)
setArray('11000011')
time.sleep(slow_time)
setArray('11100111')
time.sleep(slow_time)
setArray('01111110')
time.sleep(slow_time)
setArray('00111100')
time.sleep(slow_time)
setArray('00011000')
time.sleep(slow_time)
setArray('00100100')
time.sleep(slow_time)
setArray('01000010')
time.sleep(slow_time)
setArray('10000001')
time.sleep(slow_time)
for i in range(9):
    setNumber(i)
    time.sleep(quick_time)
for i in range(8):
    setNumber(8 - i)
    time.sleep(quick_time)

setArray('00000000')
gpio.cleanup()
sys.exit()
