#!/usr/bin/env python3
import pyaudio
import json
def getaudiodevices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        name = p.get_device_info_by_index(i).get('name')
        index =  p.get_device_info_by_index(i).get('index')
        print(str(index) + "    " + name)
        



#your_json = '["foo", {"bar":["baz", null, 1.0, 2]}]'
#parsed = json.loads(your_json)
#print json.dumps(parsed, indent=4, sort_keys=True)


getaudiodevices()