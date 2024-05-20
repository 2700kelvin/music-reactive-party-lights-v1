from typing import Union, Optional, List, TypeVar, Tuple, Type
import pyaudio # type: ignore

def getBlackholeIndex() -> int:
    p = pyaudio.PyAudio()
    blackhole = 'BlackHole 2ch'
    for i in range(p.get_device_count()):
        name = p.get_device_info_by_index(i).get('name')
        index =  p.get_device_info_by_index(i).get('index')
        if name == blackhole:
          return index
    raise Exception(f"Unable to find audio device {blackhole}")

print(getBlackholeIndex())