#!/usr/bin/env python3

from signal import pause

import apa
import mqtt_messages
import temperature as mqtt_handler
from clockring import ClockRing
import led_config

def main():
    # Setup the Rasp.IO LED Strings
    ledstrip = apa.Apa(led_config.numleds)  # initiate an LED strip
    ledstrip.zero_leds()
    ledstrip.write_leds()

    handlerclass = mqtt_handler.Temperature(ledstrip)
    mqtt_messages.Messages(handlerclass)

    ClockRing(ledstrip)

    pause()


if __name__ == "__main__":
    main()

print("Shouldn't get here!")
