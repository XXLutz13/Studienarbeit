import pybcapclient.bcapclient as bcapclient
import cv2
import numpy as np
from datetime import datetime


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

 # Get Camera Handler
IP = '10.50.12.88'
camera_handler = client.controller_connect('N10-W02', 'CaoProv.Canon.N10-W02', '', 'Conn=eth:'+ IP +', Timeout=3000')
client = client

for x in range(50):
    # OneShot
    client.controller_execute(camera_handler, 'OneShotFocus', '')
    print("image: %s"% x)