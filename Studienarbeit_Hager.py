#----------------------------------------------------------------------------------------------------------------
#   Main script for an automated imaging tool for AI services
#
#   Author: Lutz Hager 
#   Date: 05.11.22
#
#----------------------------------------------------------------------------------------------------------------
import pybcapclient.bcapclient as bcapclient    # Denso library for Cobotta access


from adafruit_motorkit import MotorKit  # library for motor control board
from adafruit_motor import stepper

import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
import cv2
import time
import numpy as np
from datetime import datetime

kit = MotorKit()    # MotorKit Object

#----------------------------------------------------------------------------------------------------------------
#   function for calculation of Roboter coordinates
#   Inputs: number of Images: num_images
#   Outputs: array of coordinats: cords
#            number of motor stepps: num_steps
#----------------------------------------------------------------------------------------------------------------
def coordinates(num_images):

    cords = []
    num_steps = []

    return cords, num_steps



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
        logging.info('Open Connection')

        # start b_cap Service
        client.service_start("")
        logging.info('started b_cap service')

        # set Parameter
        Name = ""
        Provider = "CaoProv.DENSO.VRC"
        Machine = IP
        Option = ""

        # Connect to RC8 (RC8(VRC)provider)
        RC8 = client.controller_connect(Name, Provider, Machine, Option)
        logging.info('established RC8 connection')

        return client, RC8

    except:
        logging.error("can't connect to Cobotta")

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
            logging.error("can't connect camera")

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
            logging.error("faild to capture image")


def get_number_of_Images():
    num_images = int(input('Number of Images: ') or '100')
    logging.info('User Input num_images: %s', num_images)
    return num_images


# converts Cobotta image to usable numpy formate 
def convert_image(img):
    nparry = np.frombuffer(img , dtype=np.uint8)
    cv_image = cv2.imdecode(nparry, cv2.IMREAD_COLOR)
    return cv_image

# moves stepper motor
def stepper_worker(stepper, numsteps, direction):
    for x in numsteps:
         stepper.onestep(direction=direction)


# establish Cobotta connection
client, RC8 = connect_Cobotta('10.50.12.87')
# open camera connection
CAM = CAMERA(client=client, IP='10.50.12.88')

num_images = get_number_of_Images()

# calculate arrays with roboter coordinates
cords, motorStepps = coordinates(num_images)


I90_access = client.controller_getvariable(RC8, "I90", "")   # Object for variable access
I91_access = client.controller_getvariable(RC8, "I91", "")   # Object for variable access
P90_access = client.controller_getvariable(RC8, "P90", "")   # Object to post new Coordinates

try:
    for x in num_images:

        new_coords = cords[x]   # new coordinates for robot
        client.variable_putvalue(P90_access, new_coords)    # write new coordinates

        # acctivate script on cobotta
        I90 = 1   # new value
        client.variable_putvalue(I90_access, I90) # write I90 value

        stepper_worker(kit.stepper1, motorStepps[x], stepper.FORWARD)   # move stepper motor 

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


except KeyboardInterrupt:
    # finish script on cobotta
    I90 = 0   # new value
    client.variable_putvalue(I90_access, I90) # write I90 value

    client.variable_release(I90_access)
    client.variable_release(I91_access)
    client.variable_release(P90_access)
    client.service_stop()

    kit.stepper1.release()

    logging.error("service stoped!")





