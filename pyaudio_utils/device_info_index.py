#!/usr/bin/env python3

import pyaudio



p=pyaudio.PyAudio()

print(p.get_device_info_by_index(0))