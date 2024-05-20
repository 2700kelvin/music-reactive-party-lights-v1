from typing import Union, Optional, List, TypeVar, Tuple, Type
import time
import math

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def generateManual(numLeds, musicColorArray, setColor):
    outputLedColorArray: List[float] = [0.0] * (numLeds * 3)
    for ledNum in range(numLeds):
        h = setColor[0]
        s = setColor[1]
        v = setColor[2]
        outputLedColorArray[ledNum * 3 + 0] = h
        outputLedColorArray[ledNum * 3 + 1] = s
        outputLedColorArray[ledNum * 3 + 2] = v
    return outputLedColorArray

def generateColorBeats(numLeds: int, ledColorArray: List[float], setColor: List[float], allBinsMax: float, ledAverage: float):
    magicalScalingRatio = 5 * setColor[2] # brightness
    outputLedColorArray: List[float] = [0.0] * (numLeds * 3)

    for ledNum in range(numLeds):
        ledVal = ledAverage * magicalScalingRatio  / allBinsMax

        h = setColor[0]
        s = setColor[1]
        v = ledVal
        outputLedColorArray[ledNum * 3 + 0] = h
        outputLedColorArray[ledNum * 3 + 1] = s
        outputLedColorArray[ledNum * 3 + 2] = v
    return outputLedColorArray 
def generateLightRainbowBeats(numLeds: int, ledColorArray: List[float],setColor: List[float], allBinsMax: float, ledAverage: float):
    if len(ledColorArray) != numLeds:
        raise Exception('Length of led color array wrong')
    brightness = setColor[2]
    outputLedColorArray: List[float] = [0.0] * (numLeds * 3)
    for ledNum in range(numLeds):
        ledVal = ledColorArray[ledNum] / allBinsMax

        h = ledVal
        s = 1
        v = brightness
        outputLedColorArray[ledNum * 3 + 0] = h
        outputLedColorArray[ledNum * 3 + 1] = s
        outputLedColorArray[ledNum * 3 + 2] = v
    return outputLedColorArray

def generatePulse(numLeds: int, ledColorArray: List[float],setColor: List[float], allBinsMax: float, ledAverage: float, lastPulseTime: float):
    timeSinceLastPulse = time.time() - lastPulseTime

    outputLedColorArray: List[float] = [0.0] * (numLeds * 3)
    pulseBrightness = 1.0 - clamp((timeSinceLastPulse * 2), 0,1.0)
    for ledNum in range(numLeds):
        # ledVal = ledColorArray[ledNum] / allBinsMax
        # h = ledVal
        # s = 1
        # v = pulseBrightness
        outputLedColorArray[ledNum * 3 + 0] = setColor[0]
        outputLedColorArray[ledNum * 3 + 1] = setColor[1]
        outputLedColorArray[ledNum * 3 + 2] = pulseBrightness * setColor[2]
    return outputLedColorArray

def generateIndividualColours(numLeds, setColor, individualColours):
    numFaders = len(individualColours)
    outputLedColorArray: List[float] = [0.0] * (numLeds * 3)

    for ledNum in range(numLeds):
        # ledVal = ledColorArray[ledNum] / allBinsMax
        # h = ledVal
        # s = 1
        # v = pulseBrightness

        faderIndex = math.floor(ledNum / numFaders)
        ourFader = individualColours[faderIndex]
        # print("OurFader:", ourFader)

        outputLedColorArray[ledNum * 3 + 0] = ourFader
        outputLedColorArray[ledNum * 3 + 1] = setColor[1]
        outputLedColorArray[ledNum * 3 + 2] = setColor[2]
    return outputLedColorArray

