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
import numpy as np
from datetime import datetime



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


class CAMERA:
    def __init__(self, client, IP):
        # Get Camera Handler
        camera_handler = self.client.controller_connect('N10-W02', 'CaoProv.Canon.N10-W02', '', 'Conn=eth:'+ self.IP +', Timeout=3000')
        print ('Camera handler is {}.'.format(camera_handler))

    def OneShot(self):
        image = self.client.controller_execute(self.camera_handler, 'OneShotFocus', '')

        # Get Variable ID
        variable_handler = self.client.controller_getvariable(self.camera_handler, 'IMAGE')
        print('IMAGE handler is {}.'.format(variable_handler))


        image_buff = self.client.variable_getvalue(variable_handler)

        nparr = np.frombuffer(image_buff , dtype=np.uint8)
        cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        cv2.imwrite('Images/%s_bike-yellow.png'% datetime.now().strftime("%Y%m%d_%H:%M:%S"), cv_image)



def get_number_of_Images():
    num_images = int(input('Number of Images: ') or '100')
    logging.info('User Input num_images: %s', num_images)
    return num_images


# converts Cobotta image to usable numpy formate 
def convert_image(img):
    nparry = np.frombuffer(img , dtype=np.uint8)
    cv_image = cv2.imdecode(nparry, cv2.IMREAD_COLOR)
    return cv_image




# establish Cobotta connection
client, RC8 = connect_Cobotta('10.50.12.87')

CAM = CAMERA(client=client, IP='10.50.12.88')
CAM.OneShot()

num_images = get_number_of_Images()

# calculate arrays with roboter coordinates
cords, motorStepps = coordinates(num_images)







