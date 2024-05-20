#!/usr/bin/env python3

from typing import Union, Optional, List, TypeVar, Tuple, Type

import numpy as np
import pyaudio # type: ignore
import time
import serial # type: ignore
from osc4py3.as_eventloop import * # type: ignore
from osc4py3 import oscmethod as osm #type: ignore
import threading
import socket                
import datetime
import colorsys

from color_helpers import hsvToRGBArray
from serial_helpers import getBlackholeIndex
from printing import Printing
from mode_processor import renderLeds

NUM_TILES = 4
NUM_LEDS = 150
TILE_VALUES_MULTIPLIER = 0.9
TILE_MAXIMUMS_MULTIPLIER = 0.999
MAX_VALUE = 1
# Should be the same as in the Arduino program
BAUD_RATE = 1000000
DESIRED_FRAME_RATE = 120  # FPS
# Grap this from your Arduino serial devices menu
SERIAL_PORT = '/dev/cu.usbmodem1101'
FRAME_HUE_RANGE = 0.25
HUE_INCREMENT_PER_SECOND = 1 / 60
HUE_JUMP = 3 / 8
# Adds extra text logging which does slow down event loop
DEBUG = False 
# This is the smoothness. The smaller it is the more jittery ("higher energy")
averageSamples = 5

# Chris mode / aka tile mode
TILE_CHUNK = 1024
TILE_RATE = 4410

shouldHueJump: bool = False

output_buffer = [0] * NUM_LEDS * 3

TILE_MAPPING = [0] * NUM_LEDS;

TILE_MAPPING[0] = 3
TILE_MAPPING[1] = 3
TILE_MAPPING[2] = 3
TILE_MAPPING[3] = 3
TILE_MAPPING[4] = 3
TILE_MAPPING[5] = 3
TILE_MAPPING[6] = 3
TILE_MAPPING[7] = 3
TILE_MAPPING[8] = 2
TILE_MAPPING[9] = 2
TILE_MAPPING[10] = 2
TILE_MAPPING[11] = 2
TILE_MAPPING[12] = 2
TILE_MAPPING[13] = 2
TILE_MAPPING[14] = 2
TILE_MAPPING[15] = 2
TILE_MAPPING[16] = 1
TILE_MAPPING[17] = 1
TILE_MAPPING[18] = 1
TILE_MAPPING[19] = 1
TILE_MAPPING[20] = 1
TILE_MAPPING[21] = 1
TILE_MAPPING[22] = 1
TILE_MAPPING[23] = 1
TILE_MAPPING[24] = 1
TILE_MAPPING[25] = 0
TILE_MAPPING[26] = 0
TILE_MAPPING[27] = 0
TILE_MAPPING[28] = 0
TILE_MAPPING[29] = 0
TILE_MAPPING[30] = 0
TILE_MAPPING[31] = 0
TILE_MAPPING[32] = 0
TILE_MAPPING[33] = 0
TILE_MAPPING[34] = 0
TILE_MAPPING[35] = 0
TILE_MAPPING[36] = 0
TILE_MAPPING[37] = 0
TILE_MAPPING[38] = 0
TILE_MAPPING[39] = 0
TILE_MAPPING[40] = 0
TILE_MAPPING[41] = 0
TILE_MAPPING[42] = 1
TILE_MAPPING[43] = 1
TILE_MAPPING[44] = 1
TILE_MAPPING[45] = 1
TILE_MAPPING[46] = 1
TILE_MAPPING[47] = 1
TILE_MAPPING[48] = 1
TILE_MAPPING[49] = 1
TILE_MAPPING[50] = 2
TILE_MAPPING[51] = 2
TILE_MAPPING[52] = 2
TILE_MAPPING[53] = 2
TILE_MAPPING[54] = 2
TILE_MAPPING[55] = 2
TILE_MAPPING[56] = 2
TILE_MAPPING[57] = 2
TILE_MAPPING[58] = 3
TILE_MAPPING[59] = 3
TILE_MAPPING[60] = 3
TILE_MAPPING[61] = 3
TILE_MAPPING[62] = 3
TILE_MAPPING[63] = 3
TILE_MAPPING[64] = 3
TILE_MAPPING[65] = 3

TILE_MAPPING[66] = 0
TILE_MAPPING[67] = 0
TILE_MAPPING[68] = 0
TILE_MAPPING[69] = 0
TILE_MAPPING[70] = 0
TILE_MAPPING[71] = 0
TILE_MAPPING[72] = 0
TILE_MAPPING[73] = 0
TILE_MAPPING[74] = 0
TILE_MAPPING[75] = 0
TILE_MAPPING[76] = 0
TILE_MAPPING[77] = 0
TILE_MAPPING[78] = 0
TILE_MAPPING[79] = 0
TILE_MAPPING[80] = 0
TILE_MAPPING[81] = 0
TILE_MAPPING[82] = 0
TILE_MAPPING[83] = 0
TILE_MAPPING[84] = 0
TILE_MAPPING[85] = 0
TILE_MAPPING[86] = 0

TILE_MAPPING[87] = 3
TILE_MAPPING[88] = 3
TILE_MAPPING[89] = 3
TILE_MAPPING[90] = 3
TILE_MAPPING[91] = 3
TILE_MAPPING[92] = 3
TILE_MAPPING[93] = 3
TILE_MAPPING[94] = 3
TILE_MAPPING[95] = 2
TILE_MAPPING[96] = 2
TILE_MAPPING[97] = 2
TILE_MAPPING[98] = 2
TILE_MAPPING[99] = 2
TILE_MAPPING[100] = 2
TILE_MAPPING[101] = 2
TILE_MAPPING[102] = 2
TILE_MAPPING[103] = 1
TILE_MAPPING[104] = 1
TILE_MAPPING[105] = 1
TILE_MAPPING[106] = 1
TILE_MAPPING[107] = 1
TILE_MAPPING[108] = 1
TILE_MAPPING[109] = 1
TILE_MAPPING[110] = 1
TILE_MAPPING[111] = 0
TILE_MAPPING[112] = 0
TILE_MAPPING[113] = 0
TILE_MAPPING[114] = 0
TILE_MAPPING[115] = 0
TILE_MAPPING[116] = 0
TILE_MAPPING[117] = 0
TILE_MAPPING[118] = 0
TILE_MAPPING[119] = 0
TILE_MAPPING[120] = 0
TILE_MAPPING[121] = 0
TILE_MAPPING[122] = 0
TILE_MAPPING[123] = 0
TILE_MAPPING[124] = 0
TILE_MAPPING[125] = 0
TILE_MAPPING[126] = 0
TILE_MAPPING[127] = 1
TILE_MAPPING[128] = 1
TILE_MAPPING[129] = 1
TILE_MAPPING[130] = 1
TILE_MAPPING[131] = 1
TILE_MAPPING[132] = 1
TILE_MAPPING[133] = 1
TILE_MAPPING[134] = 1
TILE_MAPPING[135] = 2
TILE_MAPPING[136] = 2
TILE_MAPPING[137] = 2
TILE_MAPPING[138] = 2
TILE_MAPPING[139] = 2
TILE_MAPPING[140] = 2
TILE_MAPPING[141] = 2
TILE_MAPPING[142] = 2
TILE_MAPPING[143] = 3
TILE_MAPPING[144] = 3
TILE_MAPPING[145] = 3
TILE_MAPPING[146] = 3
TILE_MAPPING[147] = 3
TILE_MAPPING[148] = 3
TILE_MAPPING[149] = 3

def get_frequency_bins(stream):
    buffer = stream.read(TILE_CHUNK)
    data = np.frombuffer(buffer, np.int16)
    fft = np.fft.rfft(data)
    return [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft]

def get_tile_volumes(frequency_bins):
    tile_volumes = [0] * NUM_TILES
    i = -1
    tile_num = -1
    tile_max_bin = -1

    for bin_num in range(len(frequency_bins)):
        i += 1

        if i >= tile_max_bin:
            tile_num = min(tile_num + 1, NUM_TILES - 1)
            i = 0
            tile_max_bin = 2 ** tile_num

        tile_volumes[tile_num] = max(tile_volumes[tile_num], frequency_bins[bin_num])

    return tile_volumes

####### TILE MODE CODE ABOVE

ledLookupTable = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]

###### GLOBALS ##########
COLOR_BEATS = "colorBeats"
LIGHT_RAINBOW_BEATS = "lightRainbowBeats"
# Aka. Chris mode
TILE_MODE = "tile"
MANUAL = "manual"
STROBE = "strobe"
PULSE = "pulse"
HUE_JUMP_TEXT = "hueJump"
INDIVIDUAL = "individual"
oldMode:str = COLOR_BEATS
NUM_LEDS = 150
# Show text debug?

"""Number of off cycles until lights turn back on. 1 = 50% duty cycle"""
NUM_STROBE_SKIPS = 5

numMiddleLeds = 150
numFrontLeds = 120
individualColours: List[float] = [0] * 15

lastPulseTime = 0

lighttoggle = 1
globalLastLedWriteTime:float = 0

#### STATE ####
# State that stores the current colour in HSV
mode = COLOR_BEATS
globalSetColor: List[float] = [0.0,1.0,1.0]
globalStrobeFreq = 10
globalStrobeOn:List[int] = [0]
globalStrobeDuty = 1 # 1 means equal, 0.5 means less strobe
globalLastStrobeTime: List[float] = [0.0]

MAX_FRAME_RATE: float = 120
# FORMAT = pyaudio.paFloat32
FORMAT = pyaudio.paInt16 #paFloat32
CHANNELS = 2
FRAMES_PER_BUFFER = 1024
RATE = 44100

START = 0
INPUT_DEVICE_INDEX = getBlackholeIndex() 
print("input device index", INPUT_DEVICE_INDEX)

lastTime = 0
averagePosition = 0 # must be less than averageSamples
globalLastPulseTime: float = time.time()


averages = [([0] * averageSamples)[:] for x in range(150)] # type: ignore
globalLedColourArray: List[float] = []
globalLedAverage =1
globalLedColourArray = []
globalLedAverage = 1
globalAllBinsMax = 1

wave_x = 0
wave_y = 0
spec_x = 0
spec_y = 0
data: List[float] = []

current_milli_time = lambda:time.time()

printing = Printing()
# Use this for arduino
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Use this for Processing simulation
# class serialMock():
#     def __init__(self):
#         a = 5
#     def write(self,a):
#         pass

# ser = serialMock()

def writeAda():
    ser.write("A".encode('ascii'))
    ser.write("d".encode('ascii'))
    ser.write("a".encode('ascii'))

def writeGRB(r,g,b):
    ser.write(bytes([int(r),int(g),int(b)]))

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

pa = pyaudio.PyAudio()

def getAudioStream():
    return pa.open(format = FORMAT,
    channels = CHANNELS, 
    rate = RATE, 
    input = True,
    output = False,
    frames_per_buffer = FRAMES_PER_BUFFER,
    input_device_index = INPUT_DEVICE_INDEX)

stream = getAudioStream()

class myOSCServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def setSaturation(self, args):  
        globalSetColor[1] = args
    def setColorBeats(self, args):
        global mode
        print("Setting mode to colorBeats")
        mode = COLOR_BEATS
    def setLightRainbowBeats(self, args):
        global mode
        print("Setting mode to lightRainboxBeats")
        mode = LIGHT_RAINBOW_BEATS
    def setManual(self, args):
        global mode
        print("Setting mode to manual")
        mode = MANUAL
    
    def tileMode(self, args):
        global mode
        print("Setting tile mode")
        mode = TILE_MODE

    def setHueBrightness(self,new_brightness, new_hue):  
        global lastTime
        global mode
        global globalSetColor

        print(f"Setting brightness to {new_brightness} hue to {new_hue}")
        # HSV!
        globalSetColor[0] = new_hue
        globalSetColor[2] = new_brightness

    def setIndividualMode(self,path, unused, value):
        global individualColours
        global mode
        fader = int(path.split("/")[-1]) - 1 # originally 1 based
        individualColours[fader] = value[0]
        print(fader, value[0])
        unused
        mode = INDIVIDUAL

    def setPulse(self, args):
        global mode
        global globalLastPulseTime
        globalLastPulseTime = time.time()
        print(f"Setting mode to {PULSE}")
        mode = PULSE
    
    def setShouldHueJump(self, args):
        global shouldHueJump
        shouldHueJump = True

    def setStrobe(self, button_val):
        global mode
        global oldMode
        global globalLastPulseTime
        print(f"buttonVal: {button_val}")
        globalLastPulseTime = time.time()
        print(f"Setting mode to {STROBE}")
        if button_val > 0.5:
            oldMode = mode
            globalStrobeOn[0] = 1
            mode = STROBE
        else:
            print("RESETTING")
            globalStrobeOn[0] = 0
            mode = oldMode

    def run(self):
        self.board = 1

        osc_startup() # type: ignore
        osc_udp_server("0.0.0.0", 8000, "osctest") # type: ignore
        osc_method("/1/hb",self.setHueBrightness) # type: ignore
        osc_method("/2/colorBeats",self.setColorBeats) # type: ignore
        osc_method("/2/lightRainbowBeats",self.setLightRainbowBeats) # type: ignore
        osc_method(f"/2/{TILE_MODE}",self.tileMode) # type: ignore
        osc_method(f"/2/{MANUAL}", self.setManual) # type: ignore
        osc_method(f"/2/{PULSE}",self.setPulse) # type: ignore
        osc_method(f"/2/{STROBE}",self.setStrobe) # type: ignore
        osc_method(f"/2/{HUE_JUMP_TEXT}",self.setShouldHueJump) # type: ignore
        osc_method(f"/2/{INDIVIDUAL}",self.setIndividualMode, argscheme=osm.OSCARG_MESSAGEUNPACK) # type: ignore


        osc_method(f"/1/s", self.setSaturation) #type: ignore # ew all using the same handler
        
        while True:
            # print("OSC SERVER RUNNING!")
            osc_process() # type: ignore

tempStrobeVar = 1

def tileModeMain():
    global output_buffer
    global shouldHueJump
    led_hsv_values = [[0, 0, 0]] * NUM_LEDS

    tile_values = [0] * NUM_TILES
    tile_maximums = [0] * NUM_TILES
    stream = getAudioStream()

    hue_start = 0
    last_frame_time = datetime.datetime.now().timestamp()

    while True:
        if mode != TILE_MODE:
            break
        time_since_last_frame = datetime.datetime.now().timestamp() - last_frame_time
        if time_since_last_frame < 1 / DESIRED_FRAME_RATE:
            continue

        actual_frame_rate = 1 / time_since_last_frame
        if actual_frame_rate <= DESIRED_FRAME_RATE * 0.9:
            print("Frame rate too low: ", actual_frame_rate)

        if shouldHueJump == True:
            hue_start = hue_start + HUE_JUMP
            shouldHueJump = False
        # hue_jumped = False # TEMP

        try:
            frequency_bins = get_frequency_bins(stream)
        except OSError:
            stream = getAudioStream()
            continue

        tile_volumes = get_tile_volumes(frequency_bins)

        for i in range(NUM_TILES):
            tile_maximums[i] = max(tile_maximums[i] * TILE_MAXIMUMS_MULTIPLIER, tile_volumes[i])

            if tile_maximums[i] > 0:
                tile_values[i] = \
                    max(tile_values[i] * TILE_VALUES_MULTIPLIER, tile_volumes[i] / tile_maximums[i] * MAX_VALUE)
            else:
                tile_values[i] = 0

        for i in range(NUM_LEDS):
            curr_tile = TILE_MAPPING[i]

            hue = hue_start + curr_tile / NUM_TILES * FRAME_HUE_RANGE

            if i < NUM_LEDS / 2:
                hue = hue + MAX_VALUE / 2

            led_hsv_values[i] = [hue, 1, tile_values[curr_tile] * globalSetColor[2]]

        writeAda()
        for i in range(NUM_LEDS):
            [r, g, b] = colorsys.hsv_to_rgb(*led_hsv_values[i])
            output_buffer[i * 3] = int(g * 255)
            output_buffer[i * 3 + 1] = int(r * 255)
            output_buffer[i * 3 + 2] = int(b * 255)

        ser.write(bytes(output_buffer))

        last_frame_time = datetime.datetime.now().timestamp()
        hue_start = hue_start + HUE_INCREMENT_PER_SECOND / DESIRED_FRAME_RATE

class LEDClass(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global lastLedWriteTime
        global mode
        global stream
        global globalLedColourArray
        global globalLedAverage
        global globalAllBinsMax
        global globalLastLedWriteTime
        global tempStrobeVar
        strobeSkipCounter: int = 0
        while True:
            try:
                ret = stream.read(FRAMES_PER_BUFFER)
            except IOError:
                stream = getAudioStream()
                print("IOError, getting new audio stream")
                continue

            data = np.frombuffer(ret, np.int16) #float32

            ## Do FFT
            rawFft = np.fft.rfft(data)
            bins = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in rawFft]

            ledBins = [bins[n] for n in range(len(bins))[0::1]]
            
            ## Processing
            #########
            ## Do averages
            for binIndex in range(150):
                averages[binIndex].pop()
                averages[binIndex].insert(0,ledBins[binIndex])

            globalLedColourArray = [sum(binSet) / averageSamples for binSet in averages]
            globalLedAverage = sum(globalLedColourArray)/len(globalLedColourArray)
            globalAllBinsMax = max(globalLedColourArray) + 0.001

            if DEBUG:
                printing.printBins(globalLedColourArray,globalAllBinsMax)

            if mode == STROBE and time.time() - globalLastLedWriteTime > (1/MAX_FRAME_RATE):
                outputLedColorArray = [0.0] * (150 * 3)
                if tempStrobeVar == 1:
                    if strobeSkipCounter >= NUM_STROBE_SKIPS:
                        strobeSkipCounter = 0
                        for ledNum in range(150):
                            outputLedColorArray[ledNum * 3 + 0] = globalSetColor[0]
                            outputLedColorArray[ledNum * 3 + 1] = globalSetColor[1]# sat
                            outputLedColorArray[ledNum * 3 + 2] = globalSetColor[2]
                        # Turn strobe off
                        tempStrobeVar = 0
                    else:
                        strobeSkipCounter += 1
                else:
                    tempStrobeVar = 1
                rgbArray = hsvToRGBArray(outputLedColorArray)
                writeAda()
                ser.write(bytes(rgbArray))
                globalLastLedWriteTime = time.time()
            if mode == TILE_MODE:
                tileModeMain()


            elif time.time() - globalLastLedWriteTime > (1/MAX_FRAME_RATE):
                rgbArray = renderLeds(
                    mode=mode,
                    numLeds=NUM_LEDS,
                    musicColorArray=globalLedColourArray,
                    setColor=globalSetColor,
                    allBinsMax=globalAllBinsMax,
                    ledAverage=globalLedAverage,
                    lastPulseTime=globalLastPulseTime,
                    individualColours=individualColours
                )
                if rgbArray != None:
                    writeAda()
                    ser.write(bytes(rgbArray))
                    globalLastLedWriteTime = time.time()


# A server for fetching the colours from Processing
class ColourServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.s = socket.socket()          
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = 12345
        print("Socket successfully created")
        self.s.bind(('', self.port))         
        print("socket binded to ", self.port)
          
        # put the socket into listening mode 
        self.s.listen(5)      
        print("socket is listening")

    def run(self):
        global lastLedWriteTime
        global mode
        global globalLedAverage
        global stream
        global globalLedColourArray
        while True:
            print("In while True of ColourServer run")
            # Establish connection with client. 
            c, addr = self.s.accept()      
            print('Got connection from', addr)
            lastSendTime = time.time()
            while(True):
                print("In loop")
                if time.time() - lastSendTime > (1/MAX_FRAME_RATE):
                    rgbArray = renderLeds(
                        mode=mode,
                        numLeds=NUM_LEDS,
                        musicColorArray=globalLedColourArray,
                        setColor=globalSetColor,
                        allBinsMax=globalAllBinsMax,
                        ledAverage=globalLedAverage,
                        lastPulseTime=globalLastPulseTime,
                        individualColours=individualColours
                    )
                    if rgbArray != None:
                        c.send(bytearray(rgbArray)) 
                    else:
                        print("RGB array is none!")
                    lastSendTime = time.time()

oscObject = myOSCServer()

oscServerThread = myOSCServer()
ledThread = LEDClass()
# processingServerThread = ColourServer() # Use for processing

# processingServerThread.daemon = True
ledThread.daemon = True
oscServerThread.daemon = True

# Start new Threads
oscServerThread.start()
ledThread.start()
# processingServerThread.start()


# Just keep running the threads above...
while True:
    time.sleep(1)


# osc_terminate()
