import tkinter as tk

from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import matplotlib.animation as animation

import numpy as np
from numpy import pi
import pandas as pd

import threading
import tcphandler
import socketserver
import octavethread
import time

from scipy import optimize

import random

import warnings
warnings.filterwarnings("error")
## Run server : receving data from PM1000
## ref: Run Octave Parallel with Python Using Oct2py
## https://octopus.hashnode.dev/run-octave-parallel-with-python-using-oct2py

received_data = []
data_available = threading.Event()

class ServerThread(threading.Thread):

    def __init__(self, name='server-thread'):
        super(ServerThread, self).__init__(name=name)
        self.start()

    def run(self):
        #start TCP server
        tcphandler.MyTCPHandler.callback = datacallback
        HOST, PORT = "localhost", 9999
        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), tcphandler.MyTCPHandler)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

# Decouple receiving and plotting.
# Therefore data is only copied on receive, and an event is raised to trigger updating the drawing
def datacallback(data):
    received_data.append(data) #copy the data
    data_available.set() #raise event

def buffer_clear():
    received_data.clear()

# # Start the threads
othread = octavethread.OctaveThread()
sthread = ServerThread()

################ Run server end ###################
###################################################

class Spinbox(tk.Spinbox):
    def __init__(self, *args, **kwargs):
        tk.Spinbox.__init__(self, *args, **kwargs)
        self.bind('<MouseWheel>', self.mouseWheel)
        self.bind('<Button-4>', self.mouseWheel)
        self.bind('<Button-5>', self.mouseWheel)
        self.bind('<Shift-MouseWheel>', self.shiftmouseWheel)

    def mouseWheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.invoke('buttondown')

        elif event.num == 4 or event.delta == 120:
            self.invoke('buttonup')

    def shiftmouseWheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')
            self.invoke('buttondown')

        elif event.num == 4 or event.delta == 120:
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')
            self.invoke('buttonup')

class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.running = False
        self.ani = None
        self.stokesdrawmode = True

        ##### Frame 1) Display Stokes parameters & Poincare sphere

        Graph_frm = tk.Frame(self, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        Graph_frm.grid(row=1, column=1)

        self.fig = plt.Figure()
        self.fig.set_figheight(6)
        self.fig.set_figwidth(10)

        gs_fig = GridSpec(nrows=3, ncols=2, width_ratios=[1,1.5])


        self.ax1 = self.fig.add_subplot(gs_fig[0, 0])
        self.ax2 = self.fig.add_subplot(gs_fig[1, 0])
        self.ax3 = self.fig.add_subplot(gs_fig[2, 0])

        self.line1, = self.ax1.plot([], [], lw=2)
        self.line2, = self.ax2.plot([], [], lw=2)
        self.line3, = self.ax3.plot([], [], lw=2)
        self.line3_2, = self.ax3.plot([], [], lw=2, color='red')

        self.ax4 = self.fig.add_subplot(gs_fig[:, 1], projection='3d')
        # self.ax4.text2D(0.05, 0.95, "2D Text", transform=self.ax4.transAxes)

        self.PS(self.ax4)
        self.graph, = self.ax4.plot([], [], [], color='red', linestyle="", marker="o", markersize=1)
        self.line, = self.ax4.plot([], [], [], color='blue', lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=Graph_frm)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # self.maxS = 65535
        # self.minS = 0
        self.maxS = 1
        self.minS = -1
        # self.ax0.set_ylim(0, self.maxS)
        # self.ax0.set_xlim(0, 500)
        self.ax1.set_ylim(self.minS, self.maxS)
        self.ax1.set_xlim(0, 10000)
        self.ax2.set_ylim(self.minS, self.maxS)
        self.ax2.set_xlim(0, 10000)
        self.ax3.set_ylim(self.minS, self.maxS)
        self.ax3.set_xlim(0, 10000)

        #self.ax1.xlabel("data")
        self.ax1.set_ylabel("S1")
        self.ax2.set_ylabel("S2")
        self.ax3.set_ylabel("S3")

        ##### Frame 1-1) List box for calibration ####
        Listbox_Cal_frm = tk.Frame(self, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        Listbox_Cal_frm.grid(row=1, column=2)

        ##### Frame 1-1) List box for calibration ####
        Listbox_frm = tk.Frame(Listbox_Cal_frm, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        Listbox_frm.grid(row=1, column=1)

        # input SOP
        lbl = tk.Label(Listbox_frm, text="Input SOP")
        lbl.grid(row=1, column=1)
        self.lb_in_SOP = tk.Listbox(Listbox_frm, width=10, exportselection=False)
        self.lb_in_SOP.grid(row=2,column=1)
        lbl = tk.Label(Listbox_frm, text="Input SOP\n (deg)")
        lbl.grid(row=3, column=1)
        # self.inputSOP_sb = Spinbox(Listbox_frm, width=8, from_=0, to=360, increment=0.5,
        #                            wrap=True, state='readonly', justify='right')
        # self.inputSOP_sb.grid(row=4, column=1)
        self.inputSOP_ent = tk.Entry(Listbox_frm, width=8, justify='right')
        self.inputSOP_ent.insert(0, "unknown")
        self.inputSOP_ent.grid(row=4, column=1)
        # next input SOP
        lbl = tk.Label(Listbox_frm, text='next SOP\n (deg)')
        lbl.grid(row=5, column=1)
        self.nextinputSOP_ent = tk.Entry(Listbox_frm, width=8, justify='right')
        self.nextinputSOP_ent.insert(0, 0.0)
        # self.nextinputSOP_ent.config(state='disabled')
        self.nextinputSOP_ent.grid(row=6, column=1)

        # delta SOP
        lbl = tk.Label(Listbox_frm, text= u'\u0394' + 'SOP')
        lbl.grid(row=1, column=2)
        self.lb_d_SOP = tk.Listbox(Listbox_frm, width=10, exportselection=False)
        self.lb_d_SOP.grid(row=2, column=2)

        lbl = tk.Label(Listbox_frm, text=u'\u0394' + 'SOP\n (deg)')
        lbl.grid(row=3, column=2)
        self.deltaSOP_ent = tk.Entry(Listbox_frm, width=8, justify='right')
        self.deltaSOP_ent.insert(0, '0')
        self.deltaSOP_ent.grid(row=4, column=2)

        # VS3 coil current for optimization/calibration
        lbl = tk.Label(Listbox_frm, text='I_opt/cal')
        lbl.grid(row=1, column=3)
        self.lb_Ical = tk.Listbox(Listbox_frm, width=10, exportselection=False)
        self.lb_Ical.grid(row=2, column=3)

        lbl = tk.Label(Listbox_frm, text='I_opt/cal\n (kA)')
        lbl.grid(row=3, column=3)
        self.Ical_ent = tk.Entry(Listbox_frm, width=8, justify='right')
        self.Ical_ent.insert(0, '40')
        self.Ical_ent.grid(row=4, column=3)

        # FOCS response
        lbl = tk.Label(Listbox_frm, text=u'\u0394' + 'SOP/Ical')
        lbl.grid(row=1, column=4)
        self.lb_FOCSresponse = tk.Listbox(Listbox_frm, width=10, exportselection=False)
        self.lb_FOCSresponse.grid(row=2, column=4)

        lbl = tk.Label(Listbox_frm, text=u'\u0394' + 'SOP/Ical\n (deg/kA)')
        lbl.grid(row=3, column=4)
        self.FOCSresponse_ent = tk.Entry(Listbox_frm, width=8, justify='right')
        self.FOCSresponse_ent.insert(0, 0)
        self.FOCSresponse_ent.grid(row=4, column=4)

        lbl = tk.Label(Listbox_frm, text='Opt. limit')
        lbl.grid(row=5, column=4)
        self.Optlimit_ent = tk.Entry(Listbox_frm, width=8, justify='right')
        self.Optlimit_ent.insert(0, 0)
        self.Optlimit_ent.grid(row=6, column=4)

        ##### Frame 2-2) Measurement and control buttons ####
        # frm2 = tk.Frame(self, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        # # btns.pack(side=tk.LEFT)
        # frm2.grid(row=2, column=2)
        Listbox_frm.update()
        frm1_1 = tk.Frame(Listbox_Cal_frm,
                          relief=tk.GROOVE, bd=2, padx=2, pady=2)
        #frm.pack(side=tk.LEFT)
        frm1_1.grid(row=2, column=1, sticky="news")

        # frm1_1.update()
        # width_frm1_1 = 25
        # width_frm1_1 = Listbox_frm.winfo_width()
        width_frm1_1 = 31
        self.info_ent = tk.Text(frm1_1, width= width_frm1_1, height=2)
        self.info_ent.insert("end", 'Device connection check')
        self.info_ent.grid(row=1, column=1, sticky="ns", columnspan=2)

        self.Opt_btn = tk.Button(frm1_1, height=2,
                                 wraplength=80, text='Run Optimization',
                                 command=lambda: threading.Thread(target=self.run_optimization).start())
        self.Opt_btn.grid(row=2, column=1, sticky="ew", columnspan=1)
        self.Fullscan_btn = tk.Button(frm1_1, height=2,
                                 wraplength=80, text='Fullscan',
                                 command=lambda: threading.Thread(target=self.on_click_fullscan).start())
        self.Fullscan_btn.grid(row=2, column=2, sticky="ew", columnspan=1)

        self.Set_btn = tk.Button(frm1_1, height=2,
                                 wraplength=80, text='Set data',
                                 command=lambda: threading.Thread(target=self.on_click_set).start(),
                                 state='disabled')
        self.Set_btn.grid(row=3, column=1, sticky="ew")
        self.OptSet_btn = tk.Button(frm1_1, height=2,
                                    wraplength=80, text='Reset Opt. parameters',
                                    command=lambda: threading.Thread(target=self.on_click_set_opt).start())
        self.OptSet_btn.grid(row=3, column=2, sticky="ew")
        self.Cal_btn = tk.Button(frm1_1, height=2,
                                 wraplength=80, text='Calibration',
                                 command=lambda: threading.Thread(target=self.run_cal).start())
        self.Cal_btn.grid(row=4, column=1, sticky="ew", columnspan=2)


        # #### Frame 2-1) Measurement and control buttons ####
        frm1 = tk.Frame(Listbox_Cal_frm, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        # frm.pack(side=tk.LEFT)
        frm1.grid(row=3, column=1)

        lbl = tk.Label(frm1, text="Power (dBm)")
        lbl.grid(row=1, column=1)

        self.power_ent = tk.Entry(frm1, width=8, justify='right')
        self.power_ent.insert(0, '0')
        # self.points_ent.pack(side=tk.LEFT)
        self.power_ent.grid(row=1, column=2)

        lbl = tk.Label(frm1, text="DOP")
        lbl.grid(row=2, column=1)

        self.DOP_ent = tk.Entry(frm1, width=8, justify='right')
        self.DOP_ent.insert(0, '1')
        self.DOP_ent.grid(row=2, column=2)

        lbl = tk.Label(frm1, text="ellipticity")
        lbl.grid(row=3, column=1)

        self.ellSOP_ent = tk.Entry(frm1, width=8, justify='right')
        self.ellSOP_ent.insert(0, '1')
        self.ellSOP_ent.grid(row=3, column=2)

        lbl = tk.Label(frm1, text="azimuth")
        lbl.grid(row=4, column=1)

        self.aziSOP_ent = tk.Entry(frm1, width=8, justify='right')
        self.aziSOP_ent.insert(0, '1')
        self.aziSOP_ent.grid(row=4, column=2)

        self.RUN_btn = tk.Button(frm1, width=15, text='Start', command=self.on_click)
        self.RUN_btn.grid(row=5, column=1)

        self.CLEAR_btn = tk.Button(frm1, width=15, text='Clear', command=self.on_click_clear)
        self.CLEAR_btn.grid(row=5, column=2)

        self.TOGGLE_btn = tk.Button(frm1, width=15, text='STOKES/(Ell,Azi)',
                                    # command=lambda: threading.Thread(target=self.on_click_graphtoggle).start())
                                    command=self.on_click_graphtoggle)

        self.TOGGLE_btn.grid(row=6, column=1)

        self.SAVE_btn = tk.Button(frm1, width=15, text='Save', command=self.on_click_save)
        self.SAVE_btn.grid(row=7, column=1)

        self.QUIT_btn = tk.Button(frm1, width=15, text='Quit', command=self.destroy)
        self.QUIT_btn.grid(row=6, column=2)

        # self.S0 = []
        self.S1 = []
        self.S2 = []
        self.S3 = []
        self.t = []
        self.S0 = 0
        self.DOP = 0
        self.avgell = 0
        self.avgazi = 0
        self.aziSOP = []
        self.ellSOP = []
        self.L = np.array([])
        self.inputSOP = 0
        self.output_dSOP = 0
        self.nextSOP = 0
        self.isSET = False
        self.Ical = 0
        self.deltaSOP = 0
        self.FOCSresponse = 0
        self.np0 = 0
        self.np1 = 0

    def on_click_fullscan(self):


        self.lb_in_SOP.insert(0, self.nextinputSOP_ent.get())
        self.lb_d_SOP.insert(0, float(self.deltaSOP_ent.get()[:-2]))
        self.lb_Ical.insert(0, float(self.Ical_ent.get()))
        self.lb_FOCSresponse.insert(0, self.FOCSresponse_ent.get())

        nextinputSOP = self.nextinputSOP_ent.get()
        self.nextinputSOP_ent.delete(0,"end")
        self.nextinputSOP_ent.insert(0,float(nextinputSOP)+5)
        if float(nextinputSOP) >= 180.0:
            log_data = {'inputSOP': self.lb_in_SOP.get(0, "end")[::-1],
                        'deltaSOP': self.lb_d_SOP.get(0, "end")[::-1],
                        'Ical': self.lb_Ical.get(0, "end")[::-1],
                        'FOCSresponse': self.lb_FOCSresponse.get(0, "end")[::-1]}
            df = pd.DataFrame(log_data, columns=['inputSOP', 'deltaSOP', 'Ical', 'FOCSresponse'])
            df.to_csv("Fullscan_log.csv")
            self.nextinputSOP_ent.delete(0, "end")
            self.nextinputSOP_ent.insert(0, 0.0)
            self.lb_in_SOP.delete(0,"end")
            self.lb_d_SOP.delete(0,"end")
            self.lb_Ical.delete(0,"end")
            self.lb_FOCSresponse.delete(0,"end")

    def on_click_set_opt(self):
        self.Optlimit_ent.delete(0,"end")
        self.Optlimit_ent.insert(0, '%5.4f' % (float(self.FOCSresponse_ent.get())*1.05))

    def on_click_save(self):
        S = np.vstack((self.S1, self.S2, self.S3))
        np.savetxt("Stokes.csv", S.T, delimiter=',', fmt="%.9f")

    def on_click_graphtoggle(self):
        if self.stokesdrawmode == True:
            self.stokesdrawmode = False
            # self.ax1.autoscale(enable=True, axis='y')
            # self.ax2.autoscale(enable=True, axis='y')
            # self.ax3.autoscale(enable=True, axis='y')

            self.ax1.set_ylabel('azimuth (deg)')
            self.ax2.set_ylabel('ellipticity (deg)')
            self.ax3.set_ylabel('delta SOP (deg)')
            self.canvas.draw_idle()

        else:
            self.stokesdrawmode = True
            self.ax1.set_ylim(self.minS, self.maxS)
            self.ax2.set_ylim(self.minS, self.maxS)
            self.ax3.set_ylim(self.minS, self.maxS)
            self.ax1.set_ylabel('S1')
            self.ax2.set_ylabel('S2')
            self.ax3.set_ylabel('S3')
            self.canvas.draw_idle()

    def on_click_clear(self):
        self.S1 = []
        self.S2 = []
        self.S3 = []
        self.t = []
        self.S0 = 0
        self.DOP = 0

    def PS(self, ax):
        """
        plot Poincare Sphere, ver. 20/03/2020
        return:
        ax, fig
        """
        # plt.figure(constrained_layout=True)
        #    ax = Axes3D(fig)
        # ax = fig.add_subplot(projection='3d')
        # white panes
        # ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        # ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        # ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        # no ticks
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        # no panes
        ax.set_axis_off()

        # plot greed
        u = np.linspace(0, 2 * np.pi, 31)  # azimuth
        v = np.linspace(0, np.pi, 11)  # elevation
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
        # ax.set_title(label="  " + shot, loc='left', pad=-10, fontsize=8)

        #    ax.legend()

        return ax

    def on_click_set(self):
        #self.inputSOP = self.inputSOP_ent.get()
        self.inputSOP = self.nextinputSOP_ent.get()
        self.lb_in_SOP.insert(0, self.inputSOP)
        self.lb_in_SOP.selection_clear(0, "end")
        self.lb_in_SOP.selection_set(0, 0)

        self.Ical = float(self.Ical_ent.get())
        self.lb_Ical.insert(0, self.Ical)
        self.lb_Ical.selection_clear(0, "end")
        self.lb_Ical.selection_set(0, 0)

        self.deltaSOP = float(self.deltaSOP_ent.get()[:-2])
        self.lb_d_SOP.insert(0, self.deltaSOP)
        self.lb_d_SOP.selection_clear(0,"end")
        self.lb_d_SOP.selection_set(0,0)

        self.FOCSresponse = float(self.FOCSresponse_ent.get())
        self.lb_FOCSresponse.insert(0, self.FOCSresponse)
        self.lb_FOCSresponse.selection_clear(0,"end")
        self.lb_FOCSresponse.selection_set(0,0)
        # todo check if there is no error
        self.isSET = True

    def f(self, x):
        x_tmp = round(x[0]*180/pi*2)/2
        print("next azimuth of input SOP is", x_tmp, "deg")
        if x_tmp < 0:
            x_tmp = x_tmp + 360
        # self.nextinputSOP_ent.config(state='enabled')
        self.nextinputSOP_ent.delete(0, "end")
        self.nextinputSOP_ent.insert(0, x_tmp)
        # self.nextinputSOP_ent.config(state='disabled')

        while (1):
            if self.isSET == True:
                # tmp = input(" input data: ")
                tmp = -self.FOCSresponse
                print("FOCS response: ", -tmp, "deg/kA")
                self.isSET = False

                self.inputSOP_ent.delete(0, "end")
                self.inputSOP_ent.insert(0, x_tmp)

                break
            time.sleep(0.1)
        # tmp = float(tmp)*x
        # self.a = -(tmp+1)**2
        return tmp

    def run_optimization(self):
        if str(self.Opt_btn['relief']) == 'sunken':
            return
        init_polstate = np.array([[0], [pi / 6]])
        # minimum = optimize.fmin(self.f, 1)
        self.Opt_btn.config(relief="sunken",
                            state="active",
                            text="Optimization in progress"
                            )
        self.Set_btn.config(state="normal", bg='#7FFF00')
        minftol = float(self.Optlimit_ent.get())
        self.info_ent.delete("1.0", "end")
        self.info_ent.insert("1.0", ("Optimization ftol: %5.4f" % minftol))

        fmin_result = optimize.fmin(self.f, 1, maxiter=30, xtol=1,
                                    # ftol=0.015,
                                    ftol=minftol,
                                    initial_simplex=init_polstate,
                                    retall=True,
                                    full_output=1)
        self.info_ent.delete("1.0", "end")
        self.info_ent.insert("1.0", "Optimization has finished")
        log_data = {'inputSOP' : self.lb_in_SOP.get(0,"end")[::-1],
                    'deltaSOP' : self.lb_d_SOP.get(0,"end")[::-1],
                    'Ical': self.lb_Ical.get(0,"end"[::-1]),
                    'FOCSresponse': self.lb_FOCSresponse.get(0,"end")[::-1]}
        df = pd.DataFrame(log_data, columns=['inputSOP', 'deltaSOP', 'Ical', 'FOCSresponse'])
        df.to_csv("optimization_log.csv")

        self.Opt_btn.config(relief="raised",
                            state="normal",
                            text='Run Optimization')
        self.Set_btn.config(state="disabled", bg='SystemButtonFace')

    def on_click(self):
        '''the button is a start, pause and unpause button all in one
        this method sorts out which of those actions to take'''
        if self.ani is None:
            # animation is not running; start it
            return self.start()

        if self.running:
            # animation is running; pause it
            self.ani.event_source.stop()
            self.RUN_btn.config(text='Un-Pause')
        else:
            # animation is paused; unpause it
            self.ani.event_source.start()
            self.RUN_btn.config(text='Pause')
        self.running = not self.running

    def start(self):
        # self.points = int(self.points_ent.get()) + 1
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update_graph,
            # frames=self.points,
            # interval=int(self.interval.get()),
            # repeat=False)
            interval=5,
            blit=True
        )

        self.running = True
        self.RUN_btn.config(text='Pause')
        self.ani._start()
        print('started animation')

    def update_graph(self, i):
        self.get_data2()
        # self.points_ent.insert(0, str(self.S0)+"dBm")
        # self.line0.set_data(*get_data()) # update graph
        # self.line0.set_data(self.t, self.S0)  # update graph
        if self.stokesdrawmode:
            self.line1.set_data(self.t, self.S1)  # update graph
            self.line2.set_data(self.t, self.S2)  # update graph
            self.line3.set_data(self.t, self.S3)  # update graph
            self.line1.axes.set(ylim=(-1,1))
            self.line2.axes.set(ylim=(-1,1))
            self.line3.axes.set(ylim=(-1,1))
        else:
            self.line1.set_data(self.t, self.aziSOP*180/pi)  # update graph
            self.line2.set_data(self.t, self.ellSOP*180/pi)  # update graph
            self.line3.set_data(self.t, self.L*180/pi)  # update graph
            self.line3_2.set_data(self.t[[self.np0, self.np1]], self.L[[self.np0, self.np1]]*180/pi)
            self.line1.axes.set(ylim=(-180, 180))
            self.line2.axes.set(ylim=(-90, 90))
            self.line3.axes.set(ylim=(-30, 360))


        self.DOP_ent.delete(0,"end")
        self.DOP_ent.insert(0,'%6.4f' % self.DOP)
        self.power_ent.delete(0, "end")
        self.power_ent.insert(0, '%6.4f' % self.S0)

        self.graph.set_data(self.S1, self.S2)
        self.graph.set_3d_properties(self.S3)
        self.line.set_data(self.S1[[self.np0, self.np1]], self.S2[[self.np0, self.np1]])
        self.line.set_3d_properties(self.S3[[self.np0, self.np1]])

        self.ellSOP_ent.delete(0,"end")
        self.ellSOP_ent.insert(0, '%6.3f' % (self.avgell*180/np.pi) + u'\u00B0')

        self.aziSOP_ent.delete(0, "end")
        self.aziSOP_ent.insert(0, '%6.3f' % (self.avgazi*180/np.pi) + u'\u00B0')

        if np.isnan(self.L.max()) == False:
            self.deltaSOP_ent.delete(0, "end")
            self.deltaSOP_ent.insert(0, '%6.3f' % (self.L.max() *180 /np.pi) + u'\u00B0')

            self.FOCSresponse_ent.delete(0,"end")
            self.FOCSresponse_ent.insert(0, '%7.4f' % ((self.L.max() *180 /np.pi)/float(self.Ical_ent.get())) )

        # self.info_ent.delete("1.0", "end")
        # self.info_ent.insert("1.0", self.L.max())
        # self.info_ent.insert("2.0", np.isnan(self.L.max()))

        # self.
        # return self.line0, self.line1, self.line2, self.line3
        return self.line1, self.line2, self.line3, self.line3_2, self.graph, self.line

    def cal_arclength(self):
        # this equation is based on the arc length calculation between two point on the sphere
        # assuming the unit radius (r=1)
        # therefore, the result may have error when the radius of arc is less than 1
        # However, using VS3 coil with 40kA gives only 3 deg Faraday rotation (in reflection configuration)
        # The error is < 1% todo check this.

        nS = np.sqrt(self.S1**2 + self.S2**2 + self.S3**2)
        s1 = self.S1/nS
        s2 = self.S2/nS
        s3 = self.S3/nS
        self.aziSOP = np.arctan2(s2, s1)
        self.ellSOP = np.arctan2(s3, np.sqrt(s1 ** 2 + s2 ** 2))

        # finding maximum length of Arc
        # 1st try:
        # calculate the arc length from the first point of given data set
        # find the point that shows the maximum arclength from the first point

        b = np.pi / 2 - self.ellSOP[0]
        c = np.pi / 2 - self.ellSOP
        A0 = self.aziSOP[0]
        A1 = self.aziSOP
        A = A1 - A0

        tmp = np.cos(b) * np.cos(c) + np.sin(b) * np.sin(c) * np.cos(A)
        tmp[tmp > 1] = 1
        tmp[tmp < -1] = -1
        L1 = np.arccos(tmp)

        nMax = L1.argmax()

        # 2nd try:
        # let this point as a new end point of the arc
        # then calculate the arc length again

        b = np.pi / 2 - self.ellSOP[nMax]
        A0 = self.aziSOP[nMax]
        A = A1 - A0
        tmp = np.cos(b) * np.cos(c) + np.sin(b) * np.sin(c) * np.cos(A)
        tmp[tmp > 1] = 1
        tmp[tmp < -1] = -1
        L2 = np.arccos(tmp)

        # save the calculated arclength data
        # save two end point of arc
        self.L = L2
        self.np0 = nMax
        self.np1 = L2.argmax()

    def get_data2(self):
        data_available.wait()

        # anim = animation.FuncAnimation(fig, animate, init_func=init,frames=200, interval=20, blit=True)
        tmpdata = np.array(received_data)  # ~1ms
        # print(tmpdata.size)
        ndata = 128 * 2
        if tmpdata.size > ndata * 4:  # ~1ms
            # print("comecome")
            # tS0 = tmpdata[:, 0:ndata - 1]
            # self.S0 = np.hstack((self.S0, tS0.reshape(tS0.size)))
            tS1 = tmpdata[:, 0:ndata - 1]
            #self.S1 = np.hstack((self.S1, tS1.reshape(tS1.size).mean()))
            self.S1 = np.hstack((self.S1, tS1.reshape(tS1.size)[::5]))
            tS2 = tmpdata[:, ndata:ndata * 2 - 1]
            self.S2 = np.hstack((self.S2, tS2.reshape(tS2.size)[::5]))
            tS3 = tmpdata[:, ndata * 2:ndata * 3 - 1]
            self.S3 = np.hstack((self.S3, tS3.reshape(tS3.size)[::5]))

            tS0 = tmpdata[:, -2]
            tDOP = tmpdata[:, -1]
            # now = time.time()
            # print("Elapsed %f" % (time.time() - now))
            ndata_show = 10000
            nstep = 1
            # self.S0 = self.S0[-ndata_show::nstep]
            self.S1 = self.S1[-ndata_show::nstep]
            self.S2 = self.S2[-ndata_show::nstep]
            self.S3 = self.S3[-ndata_show::nstep]

            self.S0 = np.mean(tS0)
            self.DOP = np.mean(tDOP)

            self.t = np.arange(0, len(self.S1), 1)

            self.avgazi = np.arctan2(self.S2[-1] , self.S1[-1])
            self.avgell = np.arctan2(self.S3[-1] , np.sqrt(self.S1[-1] ** 2 + self.S2[-1] ** 2))
            self.cal_arclength()
            buffer_clear()
        data_available.clear()
        # return S0, S1, S2, S3
        # print("|xx")

    def get_data(self):
        data_available.wait()

        # anim = animation.FuncAnimation(fig, animate, init_func=init,frames=200, interval=20, blit=True)
        tmpdata = np.array(received_data)  # ~1ms
        # print(tmpdata.size)
        ndata = 32 * 10
        if tmpdata.size > ndata * 4:  # ~1ms
            # print("comecome")
            # tS0 = tmpdata[:, 0:ndata - 1]
            # self.S0 = np.hstack((self.S0, tS0.reshape(tS0.size)))
            tS1 = tmpdata[:, 0:ndata - 1]
            self.S1 = np.hstack((self.S1, tS1.reshape(tS1.size)))
            tS2 = tmpdata[:, ndata:ndata * 2 - 1]
            self.S2 = np.hstack((self.S2, tS2.reshape(tS2.size)))
            tS3 = tmpdata[:, ndata * 2:ndata * 3 - 1]
            self.S3 = np.hstack((self.S3, tS3.reshape(tS3.size)))

            tS0 = tmpdata[:, -2]
            tDOP = tmpdata[:, -1]
            # now = time.time()
            # print("Elapsed %f" % (time.time() - now))
            ndata_show = 500
            nstep = 1
            # self.S0 = self.S0[-ndata_show::nstep]
            self.S1 = self.S1[-ndata_show::nstep]
            self.S2 = self.S2[-ndata_show::nstep]
            self.S3 = self.S3[-ndata_show::nstep]

            self.S0 = np.mean(tS0)
            self.DOP = np.mean(tDOP)


            self.t = np.arange(0, len(self.S1), 1)

            buffer_clear()
        data_available.clear()
        # return S0, S1, S2, S3
        # print("|xx")


def main():
    root = tk.Tk()
    app = App(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()