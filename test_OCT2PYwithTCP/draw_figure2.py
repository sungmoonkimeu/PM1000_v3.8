import numpy as np
import pandas as pd
import os
import sys

from matplotlib import pyplot as plt
from matplotlib import use
use("TkAgg")  # set the backend

os.getcwd()
if os.getcwd().split('\\')[-1] != 'test_OCT2PYwithTCP':
    os.chdir(os.getcwd() + '/test_OCT2PYwithTCP')

filename_fullscan = ["./SCK_PC-45_Stokeslog/Fullscan_log.csv"]

filename_opti = ["optimization_log_3_PC-45.csv"]

fig, ax = plt.subplots(figsize=(5,4))
fig.canvas.manager.window.geometry("+1920+0")
plt.subplots_adjust(right=0.87)

nn = 0

df = pd.read_csv(filename_opti[nn])
inputSOP = np.array(df['inputSOP'])*2
FOCSresponse = np.array(df['FOCSresponse'])
inputSOP[inputSOP > 180] = inputSOP[inputSOP > 180]-360
inputSOP[inputSOP > 180] = inputSOP[inputSOP > 180]-360
x = inputSOP
y = FOCSresponse
# ax.plot(x*2, y*1e3*np.pi/180, '-o')
ax.scatter(x[-1],y[-1]*1e3, c='red', edgecolors='k', s =100, zorder=2, label='Start')
ax.plot(x, y*1e3, '-o',zorder=1, label='Algorithm scan')
ax.scatter(x[0],y[0]*1e3, c='blue', edgecolors='k', s =100, zorder=3, label='End')

df = pd.read_csv(filename_fullscan[nn])
inputSOP = np.array(df['inputSOP'])*2   # Using HWP --> 2 theta rotation
FOCSresponse = np.array(df['FOCSresponse'])
FOCSresponse = FOCSresponse[inputSOP<365]
inputSOP = inputSOP[inputSOP<365]
inputSOP[inputSOP > 180] = inputSOP[inputSOP > 180]-360
x = np.hstack((inputSOP[inputSOP<=0], inputSOP[inputSOP>0]))
y = np.hstack((FOCSresponse[inputSOP<=0], FOCSresponse[inputSOP>0]))
# ax.plot(x*2, y*1e3*np.pi/180, '-o')
ax.plot(x[1:], y[1:]*1e3, '-o',zorder=0, label='Simple scan')
# fig, ax = plt.subplots()



ax.legend(loc='upper left')
ax.set(xlim=(-180, 180), ylim=(0, 85))
ax.set_xlabel('Azimuth of input SOP [deg]')
ax.set_ylabel('FOCS response (deg/MA)', labelpad=10)
ax2=ax.twinx()
ax2.set(ylim=(0, 85*np.pi/180))
ax2.set_ylabel('FOCS response (rad/MA)', labelpad=10)


filename_Stokes = ["Stokes.csv", "Stokes_mod0.csv", "Stokes_pulse.csv"]
df = pd.read_csv(filename_Stokes[1], header=None)
s1, s2, s3 = df[0], df[1], df[2]

fig, ax = plt.subplots(3,1,figsize=(5,4))
plt.subplots_adjust(left=0.23, right=0.95)

fig.canvas.manager.window.geometry("+1920+0")
# plt.subplots_adjust(right=0.87)
data_n = np.linspace(1,len(s1),num=len(s1))
ax[0].plot(data_n, s1)
ax[0].set_xticks([])
ax[0].set_ylabel('s1')
ax[0].set(xlim=(0,10000))
ax[1].plot(data_n, s2)
ax[1].set_xticks([])
ax[1].set_ylabel('s2')
ax[1].set(xlim=(0,10000))
ax[2].plot(data_n, s3)
ax[2].set_ylabel('s3')
ax[2].set(xlim=(0,10000),ylim=(-1,-0.975))
ax[2].set_xlabel('data number')
fig.align_ylabels(ax)
plt.show()