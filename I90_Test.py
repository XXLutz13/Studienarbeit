import pybcapclient.bcapclient as bcapclient
import cv2
import numpy as np
from datetime import datetime


# set IP Address , Port number and Timeout of connected RC8
host = "10.50.12.87"
port = 5007
timeout = 2000

# Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
print("Open Connection")

# start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

# set Parameter
Name = ""
Provider = "CaoProv.DENSO.VRC"
Machine = "10.50.12.87"
Option = ""

# Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect RC8")

I90_access = m_bcapclient.controller_getvariable(hCtrl, "I90", "")   # Object for variable access

for x in range(50):
    I90 = x + 2   # new value
    m_bcapclient.variable_putvalue(I90_access, I90) # write I90 value
    print("now: %s"% I90)