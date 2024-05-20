import colorsys
from typing import Union, Optional, List, TypeVar, Tuple, Type

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def hsvToRGBArray(hsvColorArray: List[float]):
  """Convert 0-1 range HSV to 0-255 RGB array"""
  arrayLen = len(hsvColorArray)
  numLeds = int(arrayLen / 3)
  rgbColorArray = [0] * arrayLen
  for i in range(numLeds):
    first = i * 3 + 0
    second = i * 3 + 1
    third = i * 3 + 2
    h = hsvColorArray[first]
    s = hsvColorArray[second]
    v = hsvColorArray[third]
    rgbFloat = colorsys.hsv_to_rgb(h,s,v)

    rgb = [int(clamp(colour * 255,0,255)) for colour in rgbFloat] 

    rgbColorArray[first] = rgb[1]
    rgbColorArray[second] = rgb[0]
    rgbColorArray[third] = rgb[2]
    # rgbColorArray[first] = rgb[0]
    # rgbColorArray[second] = rgb[1]
    # rgbColorArray[third] = rgb[2]
  return rgbColorArray

