#----------------------------------------------------------------------------------------------------------------
#   Test script matplotlib
#
#   Author: Lutz Hager 
#   Date: 01.11.22
#
#----------------------------------------------------------------------------------------------------------------

from cmath import cos, pi, sin

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np


r = 1
c = 1.5
number_of_ponits = 10
µ = np.linspace(0, 1, num=number_of_ponits)
x = y = z = np.zeros_like(µ)

# for i in range(number_of_ponits):
#     x[i] = np.real(r*cos(µ[i])*cos(c*µ[i]))
#     y[i] = np.real(r*sin(µ[i])*sin(c*µ[i]))
#     z[i] = np.real(r*cos(µ[i]))

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(x,y,z)
plt.show()
