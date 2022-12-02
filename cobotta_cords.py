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

def getCoords(num_images, center):
    Object_cords = [190, -40, 120]
    R = 80
    spacing = num_images//8

    # phi = np.linspace(0, 0.5 * np.pi, spacing)
    phi = np.linspace(0.5*np.pi, np.pi, spacing)
    X = []
    Y = Object_cords[1] + R * np.cos(phi)
    Z = Object_cords[2] + R * np.sin(phi)
    rx = []
    ry = []
    rz = []

    cords = []
    angle_x_increment = 90/(spacing-1)
    for i in range(spacing):
        X.append(Object_cords[0])
        rx.append(180 - i*angle_x_increment)
        ry.append(0)
        rz.append(0)
        cords.append([X[i], float(-Y[i]), float(Z[i]), rx[i], ry[i], rz[i]])

    num_steps = []
    for x in range(8):
        num_steps += [50]
    
    return cords, num_steps

Objekt_cords = [190, -40, 120]
cords, motorStepps = getCoords(100, Objekt_cords)




try:
    for x in cords:

        new_coords = x

        print(new_coords)
        print(type(new_coords))
        client.variable_putvalue(P90_access, new_coords)   # write new coordinates

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
