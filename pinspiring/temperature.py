import led_config


class Temperature():  # threading.Thread
    def __init__(self, ledstrip):
        self.__ledstrip = ledstrip  # The LED Strip object

    def messagehandler(self, command, params):
        """ MQTT will call this method to handle the message """
        if command.lower() == "temperature":
            self.__temperature(params)

    # ------------------------------------------------------------------------------------------------------------------
    # The Pinspiring Temperature
    # ------------------------------------------------------------------------------------------------------------------

    def __temperature(self, params):
        try:
            temperature = round(params[led_config.tempqueueparam], 0)
            colourrange = int((temperature + 8) / 8)
            pixelcount = int(1 + (temperature + 8) % 8)

            self.__ledstrip.zero_ledrange(led_config.temperatureoffset, led_config.temperatureoffset + 7)
            for pixel in range(pixelcount):
                self.__ledstrip.led_set(led_config.temperatureoffset + 7 - pixel, led_config.brightness,
                                        led_config.temperaturecolours[colourrange])
            self.__ledstrip.write_leds()
        except:
            print("Message does not have the temperature")
