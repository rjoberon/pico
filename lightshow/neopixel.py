#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Demo of NeoPixel strip on Raspberry Pi Pico
#
# Preparation: copy neopixel.mpy from bundle (https://circuitpython.org/libraries) to /media/rja/CIRCUITPY/lib/
#
# Usage: Copy neopixel.py to /media/rja/CIRCUITPY/code.py
#
# Source: https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/neopixel-leds
#
# Wiring:
# | device  | pin    | function                  | Pico |
# |---------+--------+---------------------------+------|
# | LED     | black  | GND                       | GND  |
# | strip   | red    | 5VDC                      | VBUS |
# |         | yellow | DIN                       | GP0  |
# |---------+--------+---------------------------+------|
# | RGB     | A      | rotary encoder            | GP3  |
# | rotary  | B      | rotary encoder            | GP4  |
# | encoder | C      | rotary encoder GND        | GND  |
# |         | 1      | LED red                   | -    |
# |         | 2      | LED green                 | -    |
# |         | 3      | switch                    | -    |
# |         | 4      | LED blue                  | -    |
# |         | 5      | common anode LED & switch | -    |
#
# Author: rja
#
# Changes:
# 2023-12-30 (rja)
# - added rotary encoder (which moves the rainbow)
# 2023-12-17 (rja)
# - changed DIN from GP20 to GP0 (1) and added rainbow code :-)
# 2021-12-26 (rja)
# - initial version


"""
NeoPixel example for Pico. Turns the NeoPixels red.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import time
import board
import neopixel
import rotaryio
from rainbowio import colorwheel

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 8

pixels = neopixel.NeoPixel(board.GP0, num_pixels, auto_write=False)
pixels.brightness = 0.5

# configure wiring
# rotary encoder
encoder = rotaryio.IncrementalEncoder(board.GP3, board.GP4)
# switch
#pin = digitalio.DigitalInOut(board.GP22)
#pin.direction = digitalio.Direction.INPUT
#pin.pull = digitalio.Pull.DOWN
#switch = Debouncer(pin)
# LED
#rgb = (
#    pwmio.PWMOut(board.GP21, frequency=5000, duty_cycle=2**16 - 1),
#    pwmio.PWMOut(board.GP20, frequency=5000, duty_cycle=2**16 - 1),
#    pwmio.PWMOut(board.GP19, frequency=5000, duty_cycle=2**16 - 1)
#)


def rainbow(speed):
    """Shift rainbow colors through LEDs."""
    for j in range(255):
        set_rainbow(j)
        time.sleep(speed)

def set_rainbow(j):
    """Show one rainbow position ."""
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + j
        pixels[i] = colorwheel(pixel_index & 255)
    pixels.show()


last_position = None

while True:
    # handle rotary encoder
    position = encoder.position
    if last_position is None or position != last_position:
        set_rainbow(position)
    last_position = position

    # wait
    time.sleep(0.15)
