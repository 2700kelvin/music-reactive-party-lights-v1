from typing import Union, Optional, List, TypeVar, Tuple, Type
NUM_LEDS = 150

from mode_generators import generateColorBeats, generateLightRainbowBeats, generatePulse, generateManual, generateIndividualColours
from color_helpers import hsvToRGBArray

def renderLeds(
  mode: str,
  numLeds: int,
  musicColorArray: List[float],
  setColor: List[float],
  allBinsMax: float,
  ledAverage: float,
  lastPulseTime: float,
  individualColours: List[float]
  ) -> Union[List[int], None]:
  ledColorArray: Union[List[float], None] = []
  if mode == "manual":
    ledColorArray = generateManual(numLeds, musicColorArray, setColor)
  elif mode == "lightRainbowBeats":
    ledColorArray = generateLightRainbowBeats(numLeds, musicColorArray, setColor,allBinsMax,ledAverage)
  elif mode == "colorBeats":
    ledColorArray = generateColorBeats(numLeds, musicColorArray, setColor, allBinsMax,ledAverage)
  elif mode == "pulse":
    ledColorArray = generatePulse(numLeds, musicColorArray, setColor, allBinsMax,ledAverage, lastPulseTime)
  elif mode == "individual":
    ledColorArray = generateIndividualColours(numLeds, setColor, individualColours)
  else:
    print(f"mode {mode} not recognised!")
  if ledColorArray == None:
    return None
  rgbArray = hsvToRGBArray(ledColorArray)
  return rgbArray