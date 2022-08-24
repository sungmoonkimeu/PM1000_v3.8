# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 11:50:03 2022
@author: agoussar

Updated on Apr 26 2022 
SMK has added another PS drawing method with plotly library
Please install plotly before running code

    plotly may be installed using pip:
    $ pip install plotly==5.7.0
    or conda:
    $ conda install -c plotly plotly=5.7.0

more information about plotly is here (https://plotly.com/python/getting-started/)
"""
from kaleido.scopes.plotly import PlotlyScope
import time
import pickle
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import time
import warnings
import plotly.graph_objects as go
import plotly.io as pio

start = time.time()
png_renderer = pio.renderers["png"]
png_renderer.width = 330 * 6
png_renderer.height = 330 * 6
png_renderer.scale = 1
pio.renderers.default = 'png'

plt.style.use('seaborn-whitegrid')
plt.rcParams.update({'figure.max_open_warning': 0})
warnings.filterwarnings("ignore", message="This figure includes Axes")
warnings.filterwarnings("ignore", message="This figure was using")
warnings.filterwarnings("ignore", message="Calling figure.constrained_layout")


def fnorm_Stokes(S1, S2, S3):
    #
    if len(S1) < 200:
        return [-1.0, S1, S2, S3]

    cnt = 0
    for ii in range(0, len(S1)):
        nS = np.sqrt(S1[ii] ** 2 + S2[ii] ** 2 + S3[ii] ** 2)
        if (nS > 0.5e-0):
            cnt += 1
            S1[ii] = S1[ii] / nS
            S2[ii] = S2[ii] / nS
            S3[ii] = S3[ii] / nS
        #
    nSt1 = float(cnt / len(S1))  # part of good data
    return [nSt1, S1, S2, S3]


def PS3(shot):
    '''
    plot Poincare Sphere, ver. 20/03/2020
    return:
    ax, fig
    '''
    fig = plt.figure(figsize=(6, 6))
    plt.figure(constrained_layout=True)

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


def PS4(shot='', az1=0, az2=1, el1=0.47, el2=0.51):
    '''
    plot Poincare Sphere, ver. 20/03/2020
    return:     ax, fig
    '''
    no_panes = True
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(projection='3d')
    #    ax = Axes3D(fig)
    #
    az1 = az1 * np.pi
    az2 = az2 * np.pi
    el1 = el1 * np.pi
    el2 = el2 * np.pi

    fsz = 16
    sprad = 1  # PS radius
    #
    # no panes
    if no_panes:
        ax.set_axis_off()
        distance = 1.3 * sprad
    #        ax.text(distance, 0, 0, '$S_1$', fontsize=fsz)
    #        ax.text(0, distance, 0, '$S_2$', fontsize=fsz)
    #        ax.text(0, 0, distance, '$S_3$', fontsize=fsz)

    else:
        # no ticks
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

        # white panes
        ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

        # ax Labels
        ax.set_xlabel('$S_1$', fontsize=fsz)
        ax.set_ylabel('$S_2$', fontsize=fsz)
        ax.set_zlabel('$S_3$', fontsize=fsz)
        ax.grid(True)

    # plot surface greed
    u = np.linspace(az1, az2, 61)  # azimuth
    v = np.linspace(el1, el2, 31)  # elevation

    x = sprad * np.outer(np.cos(u), np.sin(v))
    y = sprad * np.outer(np.sin(u), np.sin(v))
    z = sprad * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z,
                    color='w',  # (0.5, 0.5, 0.5, 0.0),
                    edgecolor='k',
                    linestyle=(0, (5, 5)),
                    rstride=3, cstride=3,
                    linewidth=.5, alpha=0.8, shade=0)

    # main circles
    #    ax.plot(np.sin(u), np.cos(u), np.zeros_like(u), 'g-.', linewidth=0.75)   #equator
    #    ax.plot(np.sin(u), np.zeros_like(u), np.cos(u), 'b-', linewidth=0.5)
    #    ax.plot(np.zeros_like(u), np.sin(u), np.cos(u), 'b-', linewidth=0.5)

    # axes and captions
    amp = 1.3 * sprad
    #    ax.plot([-amp, amp], [0, 0], [0, 0], 'k-.', lw=2, alpha=0.5)
    #    ax.plot([0, 0], [-amp, amp], [0, 0], 'k-.', lw=2, alpha=0.5)
    #    ax.plot([0, 0], [0, 0], [-amp, amp], 'k-.', lw=2, alpha=0.5)

    # points
    #    px = [1,-1, 0, 0, 0, 0]
    #    py = [0, 0, 1,-1, 0, 0]
    #    pz = [0, 0, 0, 0, 1,-1]

    #    ax.plot(px, py, pz,
    #       color='black', marker='o', markersize=4, alpha=1.0, linewidth=0)
    #
    max_size = 1.05 * sprad
    mf = 1.05
    #    print("xxx", x, y, z)
    #    ax.set_xlim(x[0], x[-1])
    #    ax.set_ylim(y[0], y[-1])
    #    ax.set_zlim(z[0], z[-1])

    ax.view_init(elev=90 / np.pi, azim=90 / np.pi)
    ax.set_title(label=shot, loc='left', pad=-10, fontsize=8)
    #    ax.legend()

    return ax, fig


def PS5():
    '''
    plot Poincare Sphere, ver. 26/04/2022
    return:
    fig
    '''

    u = np.linspace(0, 2 * np.pi, 61)  # azimuth
    v = np.linspace(0, np.pi, 31)  # elevation
    sprad = 1
    x = sprad * np.outer(np.cos(u), np.sin(v))
    y = sprad * np.outer(np.sin(u), np.sin(v))
    z = sprad * np.outer(np.ones(np.size(u)), np.cos(v))
    #    print(x)
    color1 = 'whitesmoke'
    color2 = 'red'
    fig = go.Figure()
    colorscale = [[0, color1], [0.5, color1], [1, color1]]
    fig.add_surface(x=x, y=y, z=z, opacity=0.4, showscale=False, colorscale=colorscale,
                    showlegend=False, lighting=dict(ambient=1))

    sprad = 1
    x = (sprad * np.outer(np.cos(u), np.sin(v)))[::3]
    y = (sprad * np.outer(np.sin(u), np.sin(v)))[::3]
    z = (sprad * np.outer(np.ones(np.size(u)), np.cos(v)))[::3]

    # draw black solid line and draw white dot --> dash line having smaller empty space than <<dash='dash'>> option
    # line_marker = dict(color='#000000', width=5, dash='dash')
    line_marker = dict(color='#000000', width=5, dash='solid')
    for xx, yy, zz in zip(x, y, z):
        fig.add_scatter3d(x=xx, y=yy, z=zz, mode='lines', line=line_marker, name='', showlegend=False)

    line_marker = dict(color='#FFFFFF', width=5, dash='dot')
    for xx, yy, zz in zip(x, y, z):
        fig.add_scatter3d(x=xx, y=yy, z=zz, mode='lines', line=line_marker, name='', showlegend=False)

    # parallels
    u = np.linspace(0, np.pi, 41)  # azimuth
    v = np.linspace(0, 2 * np.pi, 81)  # elevation
    sprad = 1
    x = (sprad * np.outer(np.sin(u), np.cos(v)))[::4]
    y = (sprad * np.outer(np.sin(u), np.sin(v)))[::4]
    z = (sprad * np.outer(np.cos(u), np.ones(np.size(v))))[::4]

    # draw black solid line and draw white dot --> dash line having smaller empty space than <<dash='dash'>> option
    line_marker = dict(color='#000000', width=5, dash='solid')
    for xx, yy, zz in zip(x, y, z):
        fig.add_scatter3d(x=xx, y=yy, z=zz, mode='lines', line=line_marker, name='', showlegend=False)

    line_marker = dict(color='#FFFFFF', width=5, dash='dot')
    for xx, yy, zz in zip(x, y, z):
        fig.add_scatter3d(x=xx, y=yy, z=zz, mode='lines', line=line_marker, name='', showlegend=False)

    # axes and captions
    amp = 1.2 * sprad

    line_marker2 = dict(color='#000000', width=5, dash='dashdot')
    fig.add_scatter3d(x=[-amp, amp], y=[0, 0], z=[0, 0], mode='lines', line=line_marker2,
                      name='', showlegend=False)
    fig.add_scatter3d(x=[0, 0], y=[-amp, amp], z=[0, 0], mode='lines', line=line_marker2,
                      name='', showlegend=False)
    fig.add_scatter3d(x=[0, 0], y=[0, 0], z=[-amp, amp], mode='lines', line=line_marker2,
                      name='', showlegend=False)

    distance = 1.2 * sprad
    fig.add_scatter3d(x=[distance], y=[0], z=[0], text='S<sub>1</sub>',
                      mode="text",
                      textposition="top right",
                      textfont=dict(size=18*4), showlegend=False)
    fig.add_scatter3d(x=[0], y=[distance], z=[0], text='S<sub>2</sub>',
                      mode="text",
                      textposition="top right",
                      textfont=dict(size=18*4), showlegend=False)
    fig.add_scatter3d(x=[0], y=[0], z=[distance], text='S<sub>3</sub>',
                      mode="text",
                      textposition="middle right",
                      textfont=dict(size=18*4), showlegend=False)

    fig.add_scatter3d(x=[-sprad, sprad], y=[0, 0], z=[0, 0], mode="markers",
                      marker=dict(color='#000000', size=2), showlegend=False)
    fig.add_scatter3d(x=[0, 0], y=[sprad, -sprad], z=[0, 0], mode="markers",
                      marker=dict(color='#000000', size=2), showlegend=False)
    fig.add_scatter3d(x=[0, 0], y=[0, 0], z=[sprad, -sprad], mode="markers",
                      marker=dict(color='#000000', size=2), showlegend=False)

    fig.update_layout(
        scene={
            "xaxis": {"showbackground": False, "showticklabels": False, "visible": False},
            "yaxis": {"showbackground": False, "showticklabels": False, "visible": False},
            "zaxis": {"showbackground": False, "showticklabels": False, "visible": False},
            'camera_eye': {"x": 1, "y": 1, "z": 1},
            "aspectratio": {"x": 1, "y": 1, "z": 1}
        },
        showlegend=False,
    )
    fig.update(layout_coloraxis_showscale=False)
    #    fig.show()
    return fig


def main():
    #

    # plot parameters
    #
    plt.close("all")
    plt_fmt, plt_res = '.png', 330  # 330 is max in Word'16
    plt.rcParams["axes.titlepad"] = 20  # offset for the fig title
    plt.rcParams["figure.autolayout"] = True  # tight_layout
    #  plt.rcParams['figure.constrained_layout.use'] = True  # fit legends in fig window
    fsize = 18
    plt.rc('font', size=fsize)  # controls default text sizes
    plt.rc('axes', labelsize=fsize)  # f-size of the x and y labels
    plt.rc('xtick', labelsize=fsize)  # f-size of the tick labels
    plt.rc('ytick', labelsize=fsize)  # f-size of the tick labels
    plt.rc('legend', fontsize=fsize)  # f-size legend
    plt.rc('axes', titlesize=6)  # f-size of the axes title (??)
    plt.rc('figure', titlesize=6)  # f-size of the figure title
    #

    m01_shots = [90000, 99700]
    focs_dir = 'Shots\\'
    focs_out = 'Shots-PS\\'

    dnod = {}

    for cc in m01_shots:
        plt_name = '{}{}M'.format(focs_out, str(cc))
        fin_name = '{}{:d}.pkl'.format(focs_dir, cc)
        #    print(fin_name)
        #
        dnod.clear()
        try:
            fin_pt = open(fin_name, "rb")
            dnod = pickle.load(fin_pt, encoding='Latin-1')
            fin_pt.close()
        except:
            print("{:6d}  ---    not found or error on load".format(cc))
            continue

        #    print('input:', cc, dnod.keys())
        shot = '{:6d} {:s}'.format(cc, dnod['shot-time'][0])
        shot_time = datetime.strptime(dnod['shot-time'][0], '%Y-%m-%d %H:%M:%S')
        dversion = dnod['shot-time'][1]
        print(' {:s} -- data ver: {:d}'.format(shot, dversion))

        if dversion < 4:  # load data
            #        print(dnod)
            if 'DF/G11-POW' in dnod:  # FOCS 1
                F1_in_use = True
                P1_title, F1_dt0, xdm, P1t, P1 = dnod['DF/G11-POW']
                DP1_title, av_dtx, xdm, DP1t, DP1 = dnod['DF/G11-DOP']
                S1_title, av_dtx, xdm, S1t, S1 = dnod['DF/G11-S1']
                S2_title, av_dtx, xdm, S2t, S2 = dnod['DF/G11-S2']
                S3_title, av_dtx, xdm, S3t, S3 = dnod['DF/G11-S3']
            else:
                F1_in_use = False

            if 'DF/G11-2-POW' in dnod:  # FOCS 1
                F2_in_use = True
                P2_title, F2_dt0, xdm, P2t, P2 = dnod['DF/G11-2-POW']
                DP2_title, av_dtx, xdm, DP2t, DP2 = dnod['DF/G11-2-DOP']
                D1_title, av_dtx, xdm, D1t, D1 = dnod['DF/G11-2-S1']
                D2_title, av_dtx, xdm, D2t, D2 = dnod['DF/G11-2-S2']
                D3_title, av_dtx, xdm, D3t, D3 = dnod['DF/G11-2-S3']
            else:
                F2_in_use = False
        #
        #  FOCS data
        #
        [nSt1, S1, S2, S3] = fnorm_Stokes(S1, S2, S3)
        [nDt1, D1, D2, D3] = fnorm_Stokes(D1, D2, D3)

        F1_in_use = (nSt1 > 0.5) and F1_in_use  # check number of good points
        F2_in_use = (nDt1 > 0.5) and F2_in_use

        #
        # =============== plot results for separate shots
        #
        cm = np.linspace(0, 1, len(S1))  # color map
        cm[-1] = 1.3
        #
        if (F1_in_use or F2_in_use):  # PS

            ax, fig01 = PS3(shot)

            #      fig = plt.figure(figsize=(6, 6))
            #      ax = Axes3D(fig)

            fig02 = PS5()  # draw PS using plotly

            if F1_in_use:  # F1 on PS
                ax.scatter3D(S1, S2, S3, zdir='z', marker='o', s=4, c=cm,
                             alpha=0.5, label='F1', cmap="brg")

                fig02.add_scatter3d(x=S1, y=S2, z=S3, mode="markers",
                                    marker=dict(size=6, color=cm, colorscale='amp'), name='F1')

            if F2_in_use:  # F2 on PS
                #        ax.scatter3D(D1, D2, D3, zdir='z', marker = '+', s=6, c=cm,
                #                     alpha = 0.6, label ='F2', cmap="cool")

                fig02.add_scatter3d(x=D1, y=D2, z=D3, mode="markers",
                                    marker=dict(size=6, color=cm, colorscale='ice'), name='F2')

            ax.legend()
            fig_name = plt_name + '_PS0a' + plt_fmt
            #      plt.savefig(fig_name, dpi = plt_res)
            if False:
                fig02.update_layout(showlegend=True,
                                    legend=dict(
                                        x=0.2,
                                        y=0.8,
                                        # traceorder="reversed",
                                        font=dict(
                                            family="Calibri",
                                            size=18,
                                            color="black"),
                                        itemsizing='constant'))

            fig02.update_layout(showlegend=True)
            fig02.show(renderers='png')
            #      fig02.write_image(fig_name)
            pio.write_image(fig02, fig_name, width= 330 * 6, height=330 * 6)

#      pio.write_image(fig02, fig_name )


if (__name__ == "__main__"):
    main()
    print(time.time() - start)
    plt.show()
