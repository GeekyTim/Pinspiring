#### Pinspiring - A Clock and Temperature Guage using the Rasp.IO Inspiring for the Raspberry Pi

This is a demonstration project of a simple use of the Inspiring from Rasp.io (https://rasp.io/inspiring/). 
It uses an inspiring ring for the clock and an Inspiring straight for the temperature. The current temperature is passed
to the Raspberry Pi using MQTT from any source.

The software also uses my MQTT-Messages library (https://github.com/GeekyTim/MQTT-Messages) to handle the MQTT messages.

To install, run the following:
 
    sudo apt update && sudo apt upgrade -y
    sudo apt install git -y
    cd ~
    git clone https://github.com/GeekyTim/Pinspiring.git
    sudo bash ~/Pinspiring/install.sh
    
Assuming you are starting from the latest build of the Raspberry Pi OS, this will install the required code and set up
the systemd service. 

The MQTT configuration should be edited to suit your own configuration. Edit the file code/mqtt_config.py