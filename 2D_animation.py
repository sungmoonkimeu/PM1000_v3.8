import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

x = np.arange(0, 2*np.pi, 0.1)
y = np.sin(x)

fig, ax = plt.subplots(nrows=1)

styles = ['r-', 'g-', 'y-', 'm-', 'k-', 'c-']
def plot(ax, style):
    return ax.plot(x, y, style, animated=True)[0]
lines = plot(ax, styles)

def animate(i):
    lines.set_ydata(np.sin(1*x + i/10.0))
    return lines

# We'd normally specify a reasonable "interval" here...
ani = animation.FuncAnimation(fig, animate, range(1, 200),
                              interval=0, blit=True)
plt.show()