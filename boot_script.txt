#!/bin/bash
#
# Logging
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>log.out 2>&1
#
#
#
#Startup block
sudo /bin/sleep 15
sudo /usr/bin/pigpiod
sudo /bin/sleep 1
sudo rm -r -f /pi3_weather/
sudo /bin/sleep 1
sudo git clone https://github.com/dmitrogg/pi3_weather.git /pi3_weather
sudo /bin/sleep 1
sudo chmod a+rwx /pi3_weather/pi3_weather.py
sudo /usr/bin/python3 /pi3_weather/pi3_weather.py