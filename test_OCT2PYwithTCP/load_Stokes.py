import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def draw_empty_poincare(title=None):
    """ plot empty Poincare Sphere, ver. 20/03/2020
    Created on Fri Jan 14 11:50:03 2022
    @author: agoussar
    :param title: figure title
    :return: ax of figure
    """

    fig = plt.figure(figsize=(6, 6))
    #    plt.figure(constrained_layout=True)
    ax = fig.add_subplot(projection='3d')

    # white panes
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # no ticks
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    # no panes
    ax.set_axis_off()

    # plot greed
    u = np.linspace(0, 2 * np.pi, 61)  # azimuth
    v = np.linspace(0, np.pi, 31)  # elevation
    sprad = 1
    x = sprad * np.outer(np.cos(u), np.sin(v))
    y = sprad * np.outer(np.sin(u), np.sin(v))
    z = sprad * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z,
                    color='w',  # (0.5, 0.5, 0.5, 0.0),
                    edgecolor='k',
                    linestyle=(0, (5, 5)),
                    rstride=3, cstride=3,
                    linewidth=.5, alpha=0.0, shade=0, zorder=1)

    # main circles
    ax.plot(np.sin(u), np.cos(u), np.zeros_like(u), 'g-.', linewidth=0.75, zorder=0)  # equator
    #    ax.plot(np.sin(u), np.zeros_like(u), np.cos(u), 'b-', linewidth=0.5)
    #    ax.plot(np.zeros_like(u), np.sin(u), np.cos(u), 'b-', linewidth=0.5)

    # axes and captions
    amp = 1.3 * sprad
    ax.plot([-amp, amp], [0, 0], [0, 0], 'k-.', lw=1, alpha=0.5, zorder=0)
    ax.plot([0, 0], [-amp, amp], [0, 0], 'k-.', lw=1, alpha=0.5, zorder=0)
    ax.plot([0, 0], [0, 0], [-amp, amp], 'k-.', lw=1, alpha=0.5, zorder=0)

    distance = 1.3 * sprad
    ax.text(distance, 0, 0, '$S_1$', fontsize=18)
    ax.text(0, distance, 0, '$S_2$', fontsize=18)
    ax.text(0, 0, distance, '$S_3$', fontsize=18)

    # points
    px = [1, -1, 0, 0, 0, 0]
    py = [0, 0, 1, -1, 0, 0]
    pz = [0, 0, 0, 0, 1, -1]

    ax.plot(px, py, pz,
            color='black', marker='o', markersize=4, alpha=1.0, linewidth=0, zorder=22)
    #

    max_size = 1.05 * sprad
    ax.set_xlim(-max_size, max_size)
    ax.set_ylim(-max_size, max_size)
    ax.set_zlim(-max_size, max_size)

    #    plt.tight_layout()            #not compatible
    ax.set_box_aspect([1, 1, 1])  # for the same aspect ratio

    ax.view_init(elev=90 / np.pi, azim=90 / np.pi)
    #    ax.view_init(elev=0/np.pi, azim=0/np.pi)

    ax.set_title(label=title, pad=-10, fontsize=8)

    #    ax.legend()

    return fig, ax

def cal_arclength(Stokes):
    # this equation is based on the arc length calculation between two point on the sphere
    # assuming the unit radius (r=1)
    # therefore, the result may have error when the radius of arc is less than 1
    # However, using VS3 coil with 40kA gives only 3 deg Faraday rotation (in reflection configuration)
    # The error is < 1% todo check this.
    S1, S2, S3 = Stokes.T[0], Stokes.T[1], Stokes.T[2]
    nS = np.sqrt(S1 ** 2 + S2 ** 2 + S3 ** 2)
    s1 = S1 / nS
    s2 = S2 / nS
    s3 = S3 / nS
    aziSOP = np.arctan2(s2, s1)
    ellSOP = np.arctan2(s3, np.sqrt(s1 ** 2 + s2 ** 2))

    # finding maximum length of Arc
    # 1st try:
    # calculate the arc length from the first point of given data set
    # find the point that shows the maximum arclength from the first point

    b = np.pi / 2 - ellSOP[0]
    c = np.pi / 2 - ellSOP
    A0 = aziSOP[0]
    A1 = aziSOP
    A = A1 - A0

    tmp = np.cos(b) * np.cos(c) + np.sin(b) * np.sin(c) * np.cos(A)
    tmp[tmp > 1] = 1
    tmp[tmp < -1] = -1
    L1 = np.arccos(tmp)

    nMax = L1.argmax()

    # 2nd try:
    # let this point as a new end point of the arc
    # then calculate the arc length again

    b = np.pi / 2 - ellSOP[nMax]
    A0 = aziSOP[nMax]
    A = A1 - A0
    tmp = np.cos(b) * np.cos(c) + np.sin(b) * np.sin(c) * np.cos(A)
    tmp[tmp > 1] = 1
    tmp[tmp < -1] = -1
    L2 = np.arccos(tmp)

    # save the calculated arclength data
    # save two end point of arc
    L = L2
    np0 = nMax
    np1 = L2.argmax()

    return np0, np1, L


# str = 'Stokes_-3dBm.csv'
# str = 'Stokes_-6dBm.csv'
# str = 'Stokes_-9dBm.csv'
# str = 'Stokes_-12dBm.csv'
# str = 'Stokes_-15dBm.csv'
# str = 'Stokes_-18dBm.csv'
# str = 'Stokes_-21dBm.csv'
str = 'Stokes_-27dBm.csv'
str = 'Stokes.csv'
# str = 'Stokes_-6dBm-1550nm - 1550.4nm.csv'
Stokes = np.loadtxt(str,delimiter=',')
S1, S2, S3 = Stokes.T[0], Stokes.T[1], Stokes.T[2]

x0, x1, L = cal_arclength(Stokes)
print(L.max()*180/np.pi, "degree")

fig, ax = draw_empty_poincare()
ax.plot(S1,S2,S3)
plt.show()
