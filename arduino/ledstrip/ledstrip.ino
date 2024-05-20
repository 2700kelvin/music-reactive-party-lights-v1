#include <FastLED.h>

/**
 * A simple Arduino sketch the receives lighting data over serial and displays it on a LED strip.
 * Very low quality code, but it works.
*/

/** How many LEDs in the strip */
const int numLeds = 150;

const int ledControlPin = 5;

#define SERIALRATE 1000000
#define CALIBRATION_TEMPERATURE TypicalLEDStrip  // Color correction
#define MAX_BRIGHTNESS 255 // 0-255

// A magic prefix that must be sent before the pixel data
uint8_t prefix[] = {'A', 'd', 'a'};

uint8_t hi;
uint8_t lo;
uint8_t chk;
uint8_t i;

CRGB leds[numLeds];

void setup()
{
  FastLED.addLeds<WS2812B, ledControlPin, RGB>(leds, numLeds);
  FastLED.setTemperature( CALIBRATION_TEMPERATURE );

  FastLED.setBrightness( MAX_BRIGHTNESS );

  Serial.begin(SERIALRATE);
}

void loop() {
  // wait for first byte of Magic Word
  for (i = 0; i < sizeof prefix; ++i) {
    while (!Serial.available());
waitLoop:
    if (prefix[i] == Serial.read()) {
      continue;
    }
    i = 0;
    goto waitLoop;
  }

  Serial.readBytes((char*)leds, numLeds * 3);

  for (int i = 0; i < numFrontLeds; i ++ ) {
    frontLeds[i] = leds[i];
  }

  // shows new values
  FastLED.show();
}
