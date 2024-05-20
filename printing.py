from typing import Union, Optional, List, TypeVar, Tuple, Type
import math
from shutil import get_terminal_size

class Printing():
  def __init__(self):
    terminalSize = get_terminal_size()
    self.columns = terminalSize.columns
    self.lines = terminalSize.lines

  def printBins(self,ledColorArray: List[float], allBinsMax: float):
    screenBins = [ledColorArray[n] for n in range(len(ledColorArray))[0::8]] # for i in range(len(screenBins)):
    for i in range(len(screenBins)):
        val = int(screenBins[i])
        print("#" * int(math.floor(val / allBinsMax * self.columns)-1))

    print("//////////")
    # # print("Data len:", len(data))
    # # print("rawFft:", len(rawFft))
    # print("ledColorArray len:", len(ledColorArray))
    # print("ledBins len:", len(ledBins))