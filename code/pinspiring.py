#!/usr/bin/env python3

from signal import pause

import MQTTMessages as Messages
import apa
import led_config
import mqtt_config as config
from clockring import ClockRing
from temperature import Temperature


def main():
    # Setup the Rasp.IO LED Strings
    ledstrip = apa.Apa(led_config.numleds)  # initiate an LED strip
    ledstrip.zero_leds()
    ledstrip.write_leds()

    clock = ClockRing(ledstrip)
    clock.start()

    # Set up the handler class
    handlerclass = Temperature(ledstrip)
    # Start MQTT Listener
    Messages.MQTTMessages(config.mqttconfig, handlerclass)

    handlerclass.start()

    pause()


if __name__ == "__main__":
    main()
