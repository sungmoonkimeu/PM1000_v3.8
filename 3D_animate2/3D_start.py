from mpl_toolkits import mplot3d

#matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection='3d')


# Data for a three-dimensional line
zline = [0, 1, 2, 3, 4, 5]
xline = [0, 1, 2, 3, 4, 5]
yline = [0, 1, 2, 3, 4, 5]
ax.plot3D(xline, yline, zline, 'gray')

# Data for three-dimensional scattered points
#zdata = 15 * np.random.random(100)
#xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
#ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
#ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');

plt.show()  