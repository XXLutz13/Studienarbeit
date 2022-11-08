#----------------------------------------------------------------------------------------------------------------
#   Test script matplotlib
#
#   Author: Lutz Hager 
#   Date: 01.11.22
#
#----------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np


Object_cords = [1, 2, 3]
R = 50
phi = np.linspace(0, 0.5 * np.pi, 12)
X = Object_cords[0] + R * np.cos(phi)
Y = Object_cords[1] + R * np.sin(phi)
Z = Object_cords[2] 

cords = []
for x in phi:
    cords[x] = [X[x], Y[x], Z] 

print(cords)

fig = plt.figure()
plt.axes(projection ='3d')
plt.plot(X, Y, Z, marker='o', markersize=3, color="green")
plt.grid()
plt.axis('equal')
plt.plot(1,2,3,  marker='o', markersize=3, color="red")
plt.show()
