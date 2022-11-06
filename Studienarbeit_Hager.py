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


def get_number_of_Images():
    num_images = int(input('Number of Images: ') or '100')
    logging.info('User Input num_images: %s', num_images)
    return num_images



# establish Cobotta connection
client, RC8 = connect_Cobotta('10.50.12.87')

num_images = get_number_of_Images()

# calculate arrays with roboter coordinates
cords, motorStepps = coordinates(num_images)




