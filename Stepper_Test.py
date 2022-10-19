#----------------------------------------------------------------------------------------------------------------
#   Test script for Stepper Motor on Adafruit DC and Stepper Motor HAT
#
#   Author: Lutz Hager 
#   Date: 19.10.22
#
#----------------------------------------------------------------------------------------------------------------
#sudo pip3 install adafruit-circuitpython-motorkit
# infos: https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi?view=all

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import time
import board

kit = MotorKit()

for i in range(100):
    kit.stepper1.onestep()
    time.sleep(0.01)
