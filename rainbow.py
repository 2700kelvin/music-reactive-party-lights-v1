#!/usr/bin/env python

# Rainbow mode debug. Old code, may not work.

from __future__ import print_function
import numpy as np

import serial
import colorsys
import time


ser = serial.Serial('/dev/cu.usbmodem1101', 250000)

def writeHsv(hsvDict):
    rgb = colorsys.hsv_to_rgb(hsvDict[0],hsvDict[1], hsvDict[2])
    rgbScaled = [colour * 255 for colour in rgb]
    # GRB
    ser.write(chr(int(rgbScaled[1])))
    ser.write(chr(int(rgbScaled[0])))
    ser.write(chr(int(rgbScaled[2])))



while True:
    ser.write('A')
    ser.write('d')
    ser.write('a')

    for ledNum in range(150):
        # ser.write(chr(int(ledNum/150.0 * 255.0)))
        # ser.write(chr(int(0)))
        # ser.write(chr(int(0)))
        writeHsv([ledNum / 150.0,1,1])
    time.sleep(1/60.0)

