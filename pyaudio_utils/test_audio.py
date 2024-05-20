#!/usr/bin/env python3
import pyaudio
import numpy as np
from time import sleep

CHUNK = 2**11
RATE = 44100

def peakToVal(peak):
    i = int(peak / 15)
    clamped = max(min(i, 255), 0)
    return clamped


p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=2,rate=RATE,input=True,
              frames_per_buffer=CHUNK, input_device_index=0)

for i in range(int(10*44100/1024)): #go for a few seconds
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2

    print(peakToVal(peak))
    #bars="#"*int(50*peak/2**16)
    #bars="#"*int(50*peak/2**8)
    #print("%04d %05d %s"%(i,peak,bars))

stream.stop_stream()
stream.close()
p.terminate()


