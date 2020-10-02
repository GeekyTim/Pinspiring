import threading
from signal import pause

import led_config


class Temperature(threading.Thread):  # threading.Thread
    def __init__(self, ledstrip):
        self.__ledstrip = ledstrip  # The LED Strip object

        super(Temperature, self).__init__()

    def messagehandler(self, command, params):
        """ MQTT will call this method to handle the message """
        if command.lower() == "temperature":
            temperature = params["value"]
            self.__temperature(temperature)

    def run(self):
        pause()

    def __temperature(self, outsidetemp):
        temperature = round(outsidetemp, 0)
        colourrange = int((temperature + 8) / 8)
        pixelcount = int(1 + (temperature + 8) % 8)

        self.__ledstrip.zero_ledrange(led_config.temperatureoffset,
                                      led_config.temperatureoffset + led_config.tempstrip - 1)
        for pixel in range(pixelcount):
            self.__ledstrip.led_set(led_config.temperatureoffset + led_config.tempstrip - 1 - pixel,
                                    led_config.brightness,
                                    led_config.temperaturecolours[colourrange])
        self.__ledstrip.write_leds()
