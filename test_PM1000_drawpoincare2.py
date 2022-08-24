import numpy as np
from numpy import pi
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation

##### Library for PM1000 #####
import ftd3xx as ftd3
import sys
import Python_USB
import matlab
import time
##############################


def PS3(shot):
    '''
    plot Poincare Sphere, ver. 20/03/2020
    return:
    ax, fig
    '''
    fig = plt.figure(figsize=(6, 6))
    # plt.figure(constrained_layout=True)
    #    ax = Axes3D(fig)
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
    sprad = 1.00
    x = sprad * np.outer(np.cos(u), np.sin(v))
    y = sprad * np.outer(np.sin(u), np.sin(v))
    z = sprad * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z,
                    color='w',  # (0.5, 0.5, 0.5, 0.0),
                    edgecolor='k',
                    linestyle=(0, (5, 5)),
                    rstride=3, cstride=3,
                    linewidth=.5, alpha=0.1, shade=0.0, zorder=1)

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

    ax.view_init(elev=90 / np.pi, azim=45 / np.pi)
    #    ax.view_init(elev=0/np.pi, azim=0/np.pi)

    #    ax.set_title(label = shot, loc='left', pad=10)
    ax.set_title(label="  " + shot, loc='left', pad=-10, fontsize=8)

    #    ax.legend()

    return ax, fig

def PM1000_connection(my_Novoptel):
    ########## PM 1000 Initialization  ##############
    #################################################
    # my_Novoptel = Python_USB.initialize()
    print('initpm:   ')
    #typePM      = matlab.uint16([2]) # activate for USB2.0 device
    #DevDescrPM  = "PM1000-100M-XL-FA-NN-D 44"
    typePM      = matlab.uint16([3]) # activate for USB3.0 device
    DevDescrPM  = "PM1000-100M-XL-FA-N10-D 88"
    okOut, diagnosisOut, handleoutOut, LastDevDescr_inOut, LastDevDescr_outOut = my_Novoptel.initpm(typePM,  DevDescrPM,  nargout=5)
    print(okOut, diagnosisOut, handleoutOut, LastDevDescr_inOut, LastDevDescr_outOut, sep='\n')
    print("initialization has completed")

def PM1000_readStocks1(my_Novoptel):
    S1 = (my_Novoptel.readpm(matlab.double([512+12]))-2**15)/1000
    S2 = (my_Novoptel.readpm(matlab.double([512+14]))-2**15)/1000
    S3 = (my_Novoptel.readpm(matlab.double([512+16]))-2**15)/1000
    # print(S1, S2, S3)
    # graph = ax.scatter(S1, S2, S3)
    return S1, S2, S3

def PM1000_readStocks2(my_Novoptel):

    # rdaddrIn = matlab.uint16([3], size=(1, 1))
    # addrstartIn = matlab.uint16([3], size=(1, 1))
    # addrstopIn = matlab.uint16([13], size=(1, 1))
    # wraddrIn = matlab.uint16([3], size=(1, 1))

    # rdaddrIn = matlab.uint16([0])
    # addrstartIn = matlab.uint16([0])
    # addrstopIn = matlab.double([127])
    ndata = 128
    rdaddrIn = matlab.double([0])
    addrstartIn = matlab.double([0])
    addrstopIn = matlab.double([ndata-1])
    wraddrIn1 = matlab.double([512 + 24])
    wraddrIn2 = matlab.double([512 + 25])
    wraddrIn3 = matlab.double([512 + 26])
    wraddrIn4 = matlab.double([512 + 27])


    S0, S1, S2, S3 = [], [], [], []

    for i in range(10):
        addrstartIn = matlab.double([ndata*i])
        addrstopIn = matlab.double([ndata*(i+1) - 1])
        dout1Out, OKOut1 = my_Novoptel.readburstpm(rdaddrIn, addrstartIn, addrstopIn, wraddrIn1, nargout=2)
        dout2Out, OKOut2 = my_Novoptel.readburstpm(rdaddrIn, addrstartIn, addrstopIn, wraddrIn2, nargout=2)
        dout3Out, OKOut3 = my_Novoptel.readburstpm(rdaddrIn, addrstartIn, addrstopIn, wraddrIn3, nargout=2)
        dout4Out, OKOut4 = my_Novoptel.readburstpm(rdaddrIn, addrstartIn, addrstopIn, wraddrIn4, nargout=2)

        if OKOut1 == 1:
            S0 = np.append(S0, np.array((dout1Out[0]-2**15)))
        if OKOut2 == 1:
            S1 = np.append(S1, np.array((dout2Out[0]-2**15)))
        if OKOut3 == 1:
            S2 = np.append(S2, np.array((dout3Out[0]-2**15)))
        if OKOut4 == 1:
            S3 = np.append(S3, np.array((dout4Out[0]-2**15)))


    # print(S1, S2, S3)
    # graph = ax.scatter(S1, S2, S3)
    return S0, S1, S2, S3

def PM1000_close(my_Novoptel):
    ########## PM 1000 Disconnection  ##############
    #################################################
    print('closeepm: ')
    okOut = my_Novoptel.closepm()
    print(okOut, sep='\n')
    my_Novoptel.terminate()

def update_graph(num, a, my_Novoptel):
    global S0, S1, S2, S3
    # S1, S2, S3 = a[0][num], a[1][num], a[2][num]
    #print(a[0][num])

    # S = create_Stokes('cal')
    # azi = np.random.rand(1)*pi
    # ell = np.random.rand(1) * pi
    # S.general_azimuth_ellipticity(azimuth=azi, ellipticity=ell)
    for i in range(1):
        tmpS0, tmpS1, tmpS2, tmpS3 = PM1000_readStocks2(my_Novoptel)
        S1 = np.append(S1, tmpS1)
        S2 = np.append(S2, tmpS2)
        S3 = np.append(S3, tmpS3)

    # tmpS1, tmpS2, tmpS3 = PM1000_readStocks1(my_Novoptel)
    # S1 = np.append(S1, tmpS1)
    # S2 = np.append(S2, tmpS2)
    # S3 = np.append(S3, tmpS3)

    S1 = S1[-1000:]
    S2 = S2[-1000:]
    S3 = S3[-1000:]
    #graph._offsets3d = (S1, S2, S3)
    graph.set_data(S1, S2)
    graph.set_3d_properties(S3)
    return graph,

if (__name__ == "__main__"):
    global S1, S2, S3

    my_Novoptel = Python_USB.initialize()
    PM1000_connection(my_Novoptel)
    # S1, S2, S3 = PM1000_readStocks1(my_Novoptel)
    global a
    a = []
    ax, fig = PS3('')
    #S1, S2, S3 = a[0][0], a[1][0], a[2][0]
    S1, S2, S3 = [], [], []

    # graph = ax.scatter(S1, S2, S3)
    # ani = matplotlib.animation.FuncAnimation(fig, update_graph, fargs=(a, my_Novoptel),
    #                                          interval=10, blit=False)

    graph,  = ax.plot(S1, S2, S3, linestyle="", marker="o", markersize=3)
    ani = matplotlib.animation.FuncAnimation(fig, update_graph, fargs=(a, my_Novoptel),
                                               interval=50, blit=True)
    plt.show()
    # for i in range(1000):
    #     update_graph(0, a, my_Novoptel)


    S1,S2, S3 = [], [], []
    PM1000_close(my_Novoptel)