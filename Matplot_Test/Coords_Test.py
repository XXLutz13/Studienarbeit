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

def get_number_of_Images():
    num_images = int(input('Number of Images: ') or '100')
    return num_images

def getCoords(num_images, center):
    Object_cords = [190, -40, 120]
    R = 80
    spacing = num_images//8

    # phi = np.linspace(0, 0.5 * np.pi, spacing)
    phi = np.linspace(0.5*np.pi, np.pi, spacing)
    X = []
    Y = Object_cords[1] + R * np.cos(phi)
    Z = Object_cords[2] + R * np.sin(phi)
    rx = []
    ry = []
    rz = []

    cords = []
    angle_x_increment = 90/(spacing-1)
    for i in range(spacing):
        X += [Object_cords[0]]
        rx += [180 - i*angle_x_increment]
        ry += [0]
        rz += [0]
        cords += [(X[i], -Y[i], Z[i], rx[i], ry[i], rz[i])] 

    num_steps = []
    for x in range(8):
        num_steps += [50]
    
    return cords, num_steps


num_images = get_number_of_Images()
# calculate arrays with roboter coordinates
Objekt_cords = [190, -40, 120]
cords, motorStepps = getCoords(num_images, Objekt_cords)

print(cords[0])
print(cords[11])
print(motorStepps[2])

# fig = plt.figure('Test')
# ax = plt.axes(projection ='3d')
# plt.plot(X, Y, Z, marker='o', markersize=3, color="green")
# plt.grid()
# plt.axis('equal')
# plt.plot(Object_cords[0], Object_cords[1], Object_cords[2],  marker='o', markersize=3, color="red")
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# plt.show()
