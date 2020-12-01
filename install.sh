#!/bin/bash

if [ $(id -u) -ne 0 ]; then
  printf "Script must be run as root. Try 'sudo ./install.sh'\n"
  exit 1
fi

WORKING_DIR=$(pwd)

apt update
apt install -y python3-pip
pip3 install paho.mqtt jsondict python3-spidev

git clone https://github.com/GeekyTim/MQTT-Messages.git
bash ~/MQTT-Messages/install.sh

cp ~/Pinspiring/pinspiring.service /lib/systemd/system/.
systemctl daemon-reload
systemctl enable pinspiring
systemctl start pinspiring
