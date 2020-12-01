import threading
import time
from datetime import datetime
from time import sleep

import led_config


class ClockRing(threading.Thread):
    """
    This clock works with RasPiO InsPiRing Circle

    This 12-hour clock script takes the time from the system
    and breaks it down into hours minutes and decimal seconds.

    If you have a monitor attached the time is displayed for
    every iteration of the loop.

    2 LEDs are used to show the hour in red
    1 LED is used to show the nearest 2.5 minute (60/24 = 2.5)
    1 LED denotes seconds (to the nearest 2.5)
    Every hour there is a red 'round the clock' wipe animation
    Every half hour there is a green 'round the clock' wipe animation
    Every quarter hour there is a blue 'round the clock' wipe animation

    You can tweak or customise the wipes or create new ones with
    wipe(brightness, b, g, r)
    """

    def __init__(self, strip):
        self.__ledstrip = strip
        self.__clockleds = [[led_config.brightness, 0, 0, 0]] * led_config.clockstrip

        super(ClockRing, self).__init__()

    def __wipe(self, brightness, colour):  # function for hourly etc. wipe animations
        r, g, b = colour
        for i in range(led_config.clockstrip):
            self.__ledstrip.led_set(led_config.convertled(i), brightness, (b, g, r))
            self.__ledstrip.write_leds()
            sleep(0.03)
        sleep(0.25)
        self.__ledstrip.zero_ledrange(0, led_config.clockstrip)
        self.__ledstrip.write_leds()

    def run(self):
        while True:
            timenow = datetime.now()  # grab local time from the Pi
            hour = timenow.hour  # and process into hour min sec
            if hour >= 12:
                hour = hour - 12
            minute = timenow.minute
            second = float(timenow.second + timenow.microsecond / 1000000)

            # 2 Red LEDs for the hour
            self.__ledstrip.led_set(led_config.convertled(hour * 2), led_config.brightness, led_config.colourhour)
            if hour == 0:
                self.__ledstrip.led_set(led_config.convertled(23), led_config.brightness, led_config.colourhour)
            else:
                self.__ledstrip.led_set(led_config.convertled(hour * 2 - 1), led_config.brightness,
                                        led_config.colourhour)

            # Green minute
            precise_minute = float(minute + second / 60.0)
            self.__ledstrip.led_set(led_config.convertled(int(precise_minute / 2.5)), led_config.brightness,
                                    led_config.colourminute)

            # Blue seconds
            self.__ledstrip.led_set(led_config.convertled(int(second / 2.5)), led_config.brightness,
                                    led_config.coloursecond)

            # Draw the clock
            self.__ledstrip.write_leds()

            # Now blank the LED values for all LEDs, so that if any values
            # change in the next loop iteration, we've cleaned up behind us
            self.__ledstrip.zero_ledrange(0, led_config.clockstrip)

            time.sleep(0.03)  # limit the number of cycles to ~30 fps

            if minute == 59 and int(second) == 59:  # Red wipe hourly
                self.__wipe(led_config.brightness, led_config.colourhour)

            elif minute == 29 and int(second) == 59:  # Green wipe half-hourly
                self.__wipe(led_config.brightness, led_config.coloursecond)
                # Blue wipe quarter-hourly
            elif (minute == 14 or minute == 44) and int(second) == 59:
                self.__wipe(led_config.brightness, led_config.colourminute)
