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

num_images = get_number_of_Images()
Object_cords = [50, 20, 10]
R = 50
spacing = num_images//8

# phi = np.linspace(0, 0.5 * np.pi, spacing)
phi = np.linspace(0.5*np.pi, np.pi, spacing)
X = []
Y = Object_cords[1] + R * np.cos(phi)
Z = Object_cords[2] + R * np.sin(phi)
dx = []
dy = []
dz = []

cords = []
angle_x_increment = 90/spacing
for x in range(spacing):
    X += [Object_cords[0]]
    dx += [90 - x*angle_x_increment]
    dy += [0]
    dz += [90]
    cords += [(X[x], Y[x], Z[x], dx[x], dy[x], dz[x])] 


print(cords[0])

fig = plt.figure('Test')
ax = plt.axes(projection ='3d')
plt.plot(X, Y, Z, marker='o', markersize=3, color="green")
plt.grid()
plt.axis('equal')
plt.plot(Object_cords[0], Object_cords[1], Object_cords[2],  marker='o', markersize=3, color="red")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
