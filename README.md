Low cost music-reactive party lights using Fourier transforms, Arduino and TouchOSC
=====================

> From 2017 to 2023 I built a custom music-reactive smartphone-connected lighting setup for parties and DJing that costs around $50.

Read the blog post explaining this project at  [2700kelvin.house/low-cost-music-reactive-party-lights/](https://2700kelvin.house/low-cost-music-reactive-party-lights/)).

I wasn't joking - this Python & C (Arduino code) is very low quality. I'm currently working on a
DMX-based lighting setup so I intend to spend more time on that new codebase.

Tests and improvements are very welcome!

If you hit issues feel free to email hello@2700kelvin.com or create a Github issue.
I'll try to help but I can't promise anything.

# Required components
- A WS2812-based 5V LED strip (though it's likely possibly to use any LED strip [supported by FastLED](https://github.com/FastLED/FastLED/wiki/Chipset-reference)).
- An Arduino Uno-like varient
- A power supply for the LED strip (likely a 10A 5V supply for ~150 LEDs, check your strip's specs)
- Possibly: A resistor between the Arduino data pin and the LED strip.
	- See https://forum.arduino.cc/t/arduino-ws2812b-data-pin-resistor/533031 and https://learn.sparkfun.com/tutorials/ws2812-breakout-hookup-guide/hardware-hookup for choosing this value

# Wiring
- LED strip data pin to Arduino pin 4 (or whatever you specify in `ledstrip.ino`
	- Possibly a resister here, see above pages.

# Setting up music routing
The Python program effectively takes a virtual microphone input.

The best way to do this is use a loopback utility like Blackhole which presents a virtual output
that routes to an input.

Install this utility (see below instructions), then create a new `Multi-output device` in `Audio MIDI Setup.app`.

Add BlackHole (2ch) and your desired master output (eg. `External Headphones` / `DDJ-400 Audio Out`
/ `MacBook Pro Speakers` etc). This means any audio sent into BlackHole will go into these.

# Setting up TouchOSC

- Install the TouchOSC app on your smartphone (Android/iOS, even tablets). It's paid but a very
	cool tool.
- Install the [TouchOSC Bridge]](https://hexler.net/touchosc) app on your computer (Mac/Windows).
- Open your desired interface layout from `touchosc`, and upload to your device following
	instructions in the desktop application.
- Find your computer's IP address by pressing your WiFi symbol while holding option (or your
	favourite method like `ifconfig`)
- Add this into the TouchOSC app settings
- Start the Python program below and see if events are received (it can be finnicky getting the
	setup right, sorry!)


# Installing dependencies

These may come in handy - I've written these rough notes down over the years, I can't promise they work.

PRs to improve these docs for particular architectures are very welcome.
Heavily depends on your architecture (only tested on M1 MBPs).

- `CFLAGS="-I/opt/homebrew/include -L/opt/homebrew/lib" python3 -m pip install pyaudio`
- https://stackoverflow.com/questions/33851379/how-to-install-pyaudio-on-mac-using-python-3
- Install blackhole using installer (not brew): https://existential.audio/blackhole/
- Might not be needed: Run zoom from command line so terminal requests mic access
	- http://blog.marxy.org/2021/01/apple-silicon-fldigi-but-no-sound-yet.html
- Install portaudio from source (not using brew):
		- git clone https://github.com/PortAudio/portaudio.git
		- cd portaudio
		- ./configure
		- make
		- make install
- Install numpy: may need to do:
		- sudo pip3 install numpy --compile --pre
		- May get away with a brew install numpy
- Run `setup.sh` which installs dependencies mentioned in `requirements.txt`.
- Hope for the best :)

- For m1 macs possibly: `pip3 install numpy --compile --pre`

# Notes on Python 3 pyosc
- Get diff from https://github.com/ptone/pyosc/commit/9ad134ae78fd12f290706e7e7429954dbe3fb3a2.diff
- Apply diff to pyosc repo
- https://codeinthehole.com/tips/using-pip-and-requirementstxt-to-install-from-the-head-of-a-github-branch/


# Processing integration

I wrote a Processing 3 (https://processing.org) sketch which enabled debugging with a virtual set
of lights, but I haven't verified if this works in some time.

# Authors

2700kelvin, with contributions from friends (code published under AGPLv3 with their
permission).

# License

GNU AGPLv3. See LICENSE.
