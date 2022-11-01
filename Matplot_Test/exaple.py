from cmath import pi
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

c = 1.5
r = 2
fig = plt.figure()
 
# syntax for 3-D projection
ax = plt.axes(projection ='3d')

# defining all 3 axes
z = np.linspace(0, 1, 100)
x = z * np.sin(25 * z)
y = z * np.cos(25 * z)
 
# plotting
ax.plot3D(x, y, z, 'green')
ax.set_title('3D line plot geeks for geeks')
plt.show()