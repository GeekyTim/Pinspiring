import copy
import spidev  # RasPiO Inspiring scripts

class Apa(object):
    """How it works...

    import apa

    You define the number of LEDs

    numleds = 20  and then call the class with...

    __ledstrip = apa.Apa(numleds)

    __ledstrip.__initialiseleds() sends 4 null bytes to spi 0 on CE1 to 'wake' the
    APA102c LEDs

    Then you set the values of your LEDs
    brightness, Blue, Green, Red

    __ledstrip.led_set(number, brightness, blue, green, red)
    where number is the LED position number starting at 0

    Brightness values are 0-31 for simplicity
    But you can also use  224-255 or 0xE0-0xFF

    RGB colour values are 0-255 decimal (or hex 0x00-0xFF)
    Values such as 255, 0, 0, 0 sometimes cause errors.

    If you want "black" or "off", better to use brightness of 0, 224 or 0xE0
    then the LED will be off regardless of what colour values you give it
    All LED values are stored in list variable
    led_values

    __ledstrip.write_leds() initiates the SK9822 (or APA102c) LEDs, then writes
    to spi the contents of led_values, namely 4 data bytes for each LED:
    brightness, blue, green, red

    This sets the brightness and temperaturecolours of each LED.

    After that it sends (numleds // 32) +2 iterations of null data to
    allow time for the LEDs at the end to catch up before writing to
    them again.

    Default spi speed from spidev seems to be about 330 kHz.
    This means that one transaction of 32 clock cycles, plus about 16
    of time off in between should take about 48/330000 of a second.
    Or you should be able to get 330000/48 = 6875 transactions per second.

    There are three nulls between each frame.
    With 20 LEDs you should therefore have 23 * 48/330000 = 3.3ms
    for each frame (ignoring Python processing time).
    So a theoretical 300 frames per second. But Python slows it down.

    I've noticed you can get about 100 counts per second.

    You can squash in some more by upping the MHz, but only about
    3 times as many at 60 MHz. It looks like the chip enable process
    slows things down. Perhaps xfer2 would be faster if no
    other SPI devices are in use?
    """

    def __init__(self, numleds):
        self.__numleds = numleds
        self.__led_values = [[0xE0, 0x00, 0x00, 0x00]] * self.__numleds

        self.__spi = spidev.SpiDev()
        self.__spi.open(0, 1)  # using device 1 so 0 is free for AZ
        self.__spi.max_speed_hz = 30000000  # fixing SPI (thanks Dougie)

    def __initialiseleds(self):
        """Sends 4 null bytes to wake/initiate the APA102s. Also used to terminate the frame"""
        self.__spi.xfer([0x00, 0x00, 0x00, 0x00])

    def __completesend(self):
        self.__spi.xfer([0x00, 0x00, 0x00, 0x00])
        self.__spi.xfer([0x00, 0x00, 0x00, 0x00])
        self.__spi.xfer([0x00, 0x00, 0x00, 0x00])

    def write_leds(self):
        """write_leds() writes all stored led_values to LEDs"""
        self.__initialiseleds()
        for value in self.__led_values:
            txdata = copy.copy(value)
            self.__spi.xfer(txdata)
        self.__completesend()

    def reset_leds(self):
        """reset_leds() switches all leds off manually without changing stored led_values"""
        self.__initialiseleds()
        for x in range(self.__numleds):
            self.__spi.xfer([0xE0, 0x00, 0x00, 0x00])
        self.__completesend()

    def zero_leds(self):
        """zero_leds() zeroes stored led_values without writing their values to the LEDs.
        i.e. total reset but don't display yet """
        for y in range(self.__numleds):
            self.__led_values[y] = ([0xE0, 0x00, 0x00, 0x00])

    def zero_ledrange(self, start, end):
        """zero_ledrange() zeroes stored led_values without writing their values to the LEDs.
        i.e. total reset but don't display yet"""
        for y in range(start, end):
            self.__led_values[y] = ([0xE0, 0x00, 0x00, 0x00])

    def led_set(self, number, brightness, colour):
        """led_set() is used to set the values for a specific LED.
        number is the list index of the LED e.g. first LED is 0 and eighth is 7.
        
        Brightness values are 0-31 for simplicity But you can also use  224-255 or 0xE0-0xFF
        
        Colour values are 0-255 in decimal or hex 0x00-0xFF. Values such as 255, 0, 0, 0 sometimes cause errors.
        
        If you want "black" or "off", better to use brightness of 224 or 0xE0
        then the LED will be off regardless of what colour values you give it
        """
        red, green, blue = colour
        self.__led_values[number] = [brightness, blue, green, red]
