#----------------------------------------------------------------------------------------------------------------
#   Test script for cobotta python access
#
#   Author: Lutz Hager 
#   Date: 16.11.22
#
#----------------------------------------------------------------------------------------------------------------
import pybcapclient.bcapclient as bcapclient
import cv2
import numpy as np
from datetime import datetime
import time


# set IP Address , Port number and Timeout of connected RC8
host = "10.50.12.87"
port = 5007
timeout = 2000

# Connection processing of tcp communication
client = bcapclient.BCAPClient(host, port, timeout)
print("Open Connection")

# start b_cap Service
client.service_start("")
print("Send SERVICE_START packet")

# set Parameter
Name = ""
Provider = "CaoProv.DENSO.VRC"
Machine = "10.50.12.87"
Option = ""

# Connect to RC8 (RC8(VRC)provider)
hCtrl = client.controller_connect(Name, Provider, Machine, Option)
print("Connect RC8")

I90_access = client.controller_getvariable(hCtrl, "I90", "")   # Object for variable access
I91_access = client.controller_getvariable(hCtrl, "I91", "")   # Object for variable access
P90_access = client.controller_getvariable(hCtrl, "P90", "")   # Object to post new Coordinates


try:

    new_coords = [150.5,280,200,-180,0,0]   # new coordinates for robot
    client.variable_putvalue(P90_access, new_coords)    # write new coordinates

    # acctivate script on cobotta
    I90 = 1   # new value
    client.variable_putvalue(I90_access, I90) # write I90 value
    print('skript active')

    # stepper_worker(kit.stepper1, motorStepps[x], stepper.FORWARD)   # move stepper motor 

    ready = 0
    # wait for robot to set I91
    while not ready:
        ready = client.variable_getvalue(I91_access)  # read I91
        print(ready)
        time.sleep(0.1)

    I90 = 0   # new value
    client.variable_putvalue(I90_access, I90) # write I90 value
    print("finished")

except KeyboardInterrupt:
    # finish script on cobotta
    I90 = 0   # new value
    client.variable_putvalue(I90_access, I90) # write I90 value
