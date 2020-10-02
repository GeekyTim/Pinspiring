# Clock Configuration
clockstrip = 24  # number of LEDs in our display
clockoffset = 17  # LED offset from 0
colourhour = (255, 0, 0)
colourminute = (0, 255, 0)
coloursecond = (0, 0, 255)

# Temperature Configuration
tempstrip = 8
temperatureoffset = 24
temperaturecolours = [(0, 0, 255),
                      (0, 176, 240),
                      (146, 208, 80),
                      (0, 255, 0),
                      (255, 192, 0),
                      (255, 0, 0)]

numleds = clockstrip + tempstrip
brightness = 228


def convertled(led):
    if (led < clockstrip):
        return (led + clockoffset) % clockstrip
    elif (led < numleds):
        return led
    else:
        return 0
