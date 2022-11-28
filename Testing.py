
import pybcapclient.bcapclient as bcapclient    # Denso library for Cobotta access

import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
import cv2
import time
import numpy as np
from datetime import datetime


#----------------------------------------------------------------------------------------------------------------
#   establish connection to Cobotta
#   Input: IP_adress: IP
#   Output: bcapclient: client
#           RC8 controller: RC8 
#----------------------------------------------------------------------------------------------------------------
def connect_Cobotta(IP):

    # set IP Address , Port number and Timeout of connected RC8
    host = IP
    port = 5007
    timeout = 2000

    try:
        # Connection processing of tcp communication
        client = bcapclient.BCAPClient(host, port, timeout)

        # start b_cap Service
        client.service_start("")

        # set Parameter
        Name = ""
        Provider = "CaoProv.DENSO.VRC"
        Machine = host
        Option = ""

        # Connect to RC8 (RC8(VRC)provider)
        RC8 = client.controller_connect(Name, Provider, Machine, Option)

        return client, RC8

    except:
        raise RuntimeError("can't connect to Cobotta")

#----------------------------------------------------------------------------------------------------------------
#   cobotta camera class
#   Atributes: client = Cobotta connection
#              IP = camera IP-adress
#----------------------------------------------------------------------------------------------------------------
class CAMERA:
    def __init__(self, client, IP):
        try:
            # Get Camera Handler
            self.camera_handler = client.controller_connect('N10-W02', 'CaoProv.Canon.N10-W02', '', 'Conn=eth:'+ IP +', Timeout=3000')
            self.client = client
        except:
            raise RuntimeError("can't connect camera")

    def OneShot(self):
        try:
            image = self.client.controller_execute(self.camera_handler, 'OneShotFocus', '')

            # Get Variable ID
            variable_handler = self.client.controller_getvariable(self.camera_handler, 'IMAGE')

            image_buff = self.client.variable_getvalue(variable_handler)
            # converts Cobotta image to usable numpy formate 
            nparr = np.frombuffer(image_buff , dtype=np.uint8)
            cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # save image to file
            cv2.imwrite('Images/%s_bike-yellow.png'% datetime.now().strftime("%Y%m%d_%H:%M:%S"), cv_image)
        except:
            raise RuntimeError("faild to capture image")


def getCoords():
    num_images = 100
    Object_cords = [50, 20, 10]
    R = 50
    spacing = num_images//8

    # phi = np.linspace(0, 0.5 * np.pi, spacing)
    phi = np.linspace(0.5*np.pi, np.pi, spacing)
    X = []
    Y = Object_cords[1] + R * np.cos(phi)
    Z = Object_cords[2] + R * np.sin(phi)
    dx = []
    dy = []
    dz = []

    cords = []
    angle_x_increment = 90/spacing
    for x in range(spacing):
        X += [Object_cords[0]]
        dx += [90 - x*angle_x_increment]
        dy += [0]
        dz += [90]
        cords += [(X[x], Y[x], Z[x], dx[x], dy[x], dz[x])] 


# establish Cobotta connection
client, RC8 = connect_Cobotta('10.50.12.87')
# open camera connection
CAM = CAMERA(client=client, IP='10.50.12.88')

I90_access = client.controller_getvariable(RC8, "I90", "")   # Object for variable access
I91_access = client.controller_getvariable(RC8, "I91", "")   # Object for variable access
P90_access = client.controller_getvariable(RC8, "P90", "")   # Object to post new Coordinates


for i in range(8):
    new_coords = cords[x]   # new coordinates for robot
    print(new_coords)
    client.variable_putvalue(P90_access, new_coords)    # write new coordinates

    # acctivate script on cobotta
    I90 = 1   # new value
    client.variable_putvalue(I90_access, I90) # write I90 value

    # stepper_worker(kit.stepper1, motorStepps[x], stepper.FORWARD)   # move stepper motor 

    ready = 0
    # wait for robot to set I91
    while not ready:
        ready = client.variable_getvalue(I91_access)  # read I91
        time.sleep(0.1)

    # capturing image
    CAM.OneShot()

    # evtl delay?

    # finish script on cobotta
    I90 = 0   # new value
    client.variable_putvalue(I90_access, I90) # write I90 value
