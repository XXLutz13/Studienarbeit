#----------------------------------------------------------------------------------------------------------------
#   Test script for cobotta python access
#
#   Author: Lutz Hager 
#   Date: 21.10.22
#
#----------------------------------------------------------------------------------------------------------------
import pybcapclient.bcapclient as bcapclient

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
