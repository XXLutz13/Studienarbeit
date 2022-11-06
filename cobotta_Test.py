#----------------------------------------------------------------------------------------------------------------
#   Test script for cobotta python access
#
#   Author: Lutz Hager 
#   Date: 21.10.22
#
#----------------------------------------------------------------------------------------------------------------
import pybcapclient.bcapclient as bcapclient
import cv2

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

# #------------------------------------------------------------------------

# # get Object for reading a variable from Cobotta
# # "I1" = Identifier of the variable
# IHandl = 0
# IHandl = m_bcapclient.controller_getvariable(hCtrl, "I0", "")

# # read value of a variable from Cobotta
# # "I1" = Identifier of the variable
# retI = m_bcapclient.variable_getvalue(IHandl)

# #------------------------------------------------------------------------

# # put object for writing a variable zo Cobotta
# # "I1" = Identifier of the variable
# newVal = 15
# m_bcapclient.variable_putvalue(IHandl, newVal)

# #------------------------------------------------------------------------



# example of how the robot access will be handled later
I90_access = m_bcapclient.controller_getvariable(hCtrl, "I90", "")   # Object for variable access
CobottaAccess = 1   # new value
m_bcapclient.variable_putvalue(I90_access, CobottaAccess)


P90_access = m_bcapclient.controller_getvariable(hCtrl, "P90", "")   # Object to post new Coordinates
new_coords = [0,0,0] 
m_bcapclient.variable_putvalue(P90_access, new_coords)    # write new coordinates


# Get Camera Handler
camera_handler = m_bcapclient.controller_connect('N10-W02', 'CaoProv.Canon.N10-W02', '', 'Conn=eth:10.50.12.88, Timeout=3000')
print ('Camera handler is {}.'.format(camera_handler))

# OneShot
image = m_bcapclient.controller_execute(camera_handler, 'OneShotFocus', '')

# Get Variable ID
variable_handler = m_bcapclient.controller_getvariable(camera_handler, 'IMAGE')
print('IMAGE handler is {}.'.format(variable_handler))

# Add variable(101)
image_buff = m_bcapclient.variable_getvalue(variable_handler)


cv2.imwrite('test.png', image_buff)