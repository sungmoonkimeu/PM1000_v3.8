import tkinter as tk

from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import matplotlib.animation as animation

import numpy as np
import threading
import tcphandler
import socketserver
import octavethread

from scipy import optimize

import random

## Run server : receving data from PM1000

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

# Start the threads
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

        ##### Frame 3) Display Stokes parameters

        Graph_frm = tk.Frame(self, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        # btns.pack(side=tk.LEFT)
        Graph_frm.grid(row=1, column=1)

        self.fig = plt.Figure()
        self.fig.set_figheight(6)
        self.fig.set_figwidth(10)

        gs_fig = GridSpec(nrows=3, ncols=2, width_ratios=[1,1.5])
        # self.ax0 = self.fig.add_subplot(411)
        # self.ax1 = self.fig.add_subplot(412)
        # self.ax2 = self.fig.add_subplot(413)
        # self.ax3 = self.fig.add_subplot(414)
        # self.line0, = self.ax0.plot([], [], lw=2)
        # self.line1, = self.ax1.plot([], [], lw=2)
        # self.line2, = self.ax2.plot([], [], lw=2)
        # self.line3, = self.ax3.plot([], [], lw=2)

        # self.ax1 = self.fig.add_subplot(311)
        # self.ax2 = self.fig.add_subplot(312)
        # self.ax3 = self.fig.add_subplot(313)

        self.ax1 = self.fig.add_subplot(gs_fig[0, 0])
        self.ax2 = self.fig.add_subplot(gs_fig[1, 0])
        self.ax3 = self.fig.add_subplot(gs_fig[2, 0])

        self.line1, = self.ax1.plot([], [], lw=2)
        self.line2, = self.ax2.plot([], [], lw=2)
        self.line3, = self.ax3.plot([], [], lw=2)

        self.ax4 = self.fig.add_subplot(gs_fig[:, 1], projection='3d')
        # self.ax4.text2D(0.05, 0.95, "2D Text", transform=self.ax4.transAxes)

        self.PS(self.ax4)
        self.graph, = self.ax4.plot([], [], [], color='red', linestyle="", marker="o", markersize=1)
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
        self.ax1.set_xlim(0, 2000)
        self.ax2.set_ylim(self.minS, self.maxS)
        self.ax2.set_xlim(0, 2000)
        self.ax3.set_ylim(self.minS, self.maxS)
        self.ax3.set_xlim(0, 2000)

        #self.ax1.xlabel("data")
        self.ax1.set_ylabel("S1")
        self.ax2.set_ylabel("S2")
        self.ax3.set_ylabel("S3")


        ##### Frame 1) Displaying power, DOP, control button  ####
        frm0 = tk.Frame(self, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        frm0.grid(row=2, column=1)

        frm1 = tk.Frame(frm0, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        #frm.pack(side=tk.LEFT)
        frm1.grid(row=1, column=1)

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

        self.RUN_btn = tk.Button(frm1, width=15, text='Start', command=self.on_click)
        self.RUN_btn.grid(row=3, column=1)

        self.CLEAR_btn = tk.Button(frm1, width=15, text='Clear', command=self.on_click_clear)
        self.CLEAR_btn.grid(row=3, column=2)

        lbl = tk.Label(frm1, text="ellipticity")
        lbl.grid(row=1, column=3)

        lbl = tk.Label(frm1, text="azimuth")
        lbl.grid(row=2, column=3)

        self.ellSOP_ent = tk.Entry(frm1, width=8, justify='right')
        self.ellSOP_ent.insert(0, '1')
        self.ellSOP_ent.grid(row=1, column=4)

        self.aziSOP_ent = tk.Entry(frm1, width=8, justify='right')
        self.aziSOP_ent.insert(0, '1')
        self.aziSOP_ent.grid(row=2, column=4)

        self.TOGGLE_btn = tk.Button(frm1, width=15, text='STOKES/(Ell,Azi)',
                                    #command=lambda: threading.Thread(target=self.on_click_graphtoggle).start())
                                    command=self.on_click_graphtoggle)

        self.TOGGLE_btn.grid(row=3, column=3)

        self.QUIT_btn = tk.Button(frm1, width=15, text='Quit', command=self.destroy)
        self.QUIT_btn.grid(row=3, column=4)


        # ##### Frame 2) Calibration
        # frm2 = tk.Frame(self, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        # # btns.pack(side=tk.LEFT)
        # frm2.grid(row=2, column=2)

        frm1_1 = tk.Frame(frm0, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        #frm.pack(side=tk.LEFT)
        frm1_1.grid(row=1, column=2)
        lbl = tk.Label(frm1_1, text="Input SOP")
        lbl.grid(row=1, column=1)

        lbl = tk.Label(frm1_1, text=u'\u0394' + 'SOP')
        lbl.grid(row=2, column=1)

        lbl = tk.Label(frm1_1, text='Ical (kA)')
        lbl.grid(row=3, column=1)

        #self.inputSOP_sb = tk.Entry(frm1_1, width=8, justify='right')

        # self.inputSOP_sb = tk.Spinbox(frm1_1, width=8, from_=0, to=360, validate='all',
        #                               validatecommand=validate_command,
        #                               invalidcommand=invalid_command)
        self.inputSOP_sb = Spinbox(frm1_1, width=8, from_=0, to=360, increment=0.5,
                                   wrap=True, state='readonly', justify='right')
        self.inputSOP_sb.grid(row=1, column=2)

        self.deltaSOP_ent = tk.Entry(frm1_1, width=8, justify='right')
        self.deltaSOP_ent.insert(0, '1')
        self.deltaSOP_ent.grid(row=2, column=2)

        self.Ical_ent = tk.Entry(frm1_1, width=8, justify='right')
        self.Ical_ent.insert(0, '1')
        self.Ical_ent.grid(row=3, column=2)

        lbl = tk.Label(frm1_1, width=15, text=u'\u0394' + 'SOP/Ical')
        lbl.grid(row=1, column=3)

        lbl = tk.Label(frm1_1, text='next input SOP')
        lbl.grid(row=2, column=3)

        self.Cal_btn = tk.Button(frm1_1, width=20, text='Calculate next input SOP',
                                 # command=threading.Thread(target=self.run_cal).start())
                                 # command=self.run_cal)
                                 command=lambda: threading.Thread(target=self.run_cal).start())
        self.Cal_btn.grid(row=3, column=3)

        self.FOCSresponse_ent = tk.Entry(frm1_1, width=8, justify='right')
        self.FOCSresponse_ent.insert(0, '1')
        self.FOCSresponse_ent.grid(row=1, column=4)

        self.nextinputSOP_ent = tk.Entry(frm1_1, width=8, justify='right')
        self.nextinputSOP_ent.insert(0, '1')
        self.nextinputSOP_ent.grid(row=2, column=4)

        frm1_2 = tk.Frame(frm0, relief=tk.GROOVE, bd=2, padx=2, pady=2)
        frm1_2.grid(row=1, column=3)
        lbl = tk.Label(frm1_2, text='next input SOP')
        lbl.grid(row=1, column=1)

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

    def on_click_graphtoggle(self):
        if self.stokesdrawmode == True:
            self.stokesdrawmode = False
            self.ax1.autoscale(enable=True, axis='y')
            self.ax2.autoscale(enable=True, axis='y')
            self.ax3.autoscale(enable=True, axis='y')

            self.ax1.set_ylabel('ellipticity (deg)')
            self.ax2.set_ylabel('azimuth (deg)')
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
            self.canvas.update()


    def on_click_clear(self):
        self.S1 = []
        self.S2 = []
        self.S3 = []
        self.t = []
        self.S0 = 0
        self.DOP = 0

    def PS(self,ax):
        '''
        plot Poincare Sphere, ver. 20/03/2020
        return:
        ax, fig
        '''
        # plt.figure(constrained_layout=True)
        #    ax = Axes3D(fig)
        # ax = fig.add_subplot(projection='3d')
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

    def f(self, x):
        tmp = input(" input data: ")
        tmp = int(tmp)
        self.a = (tmp+1)**2

    def run_cal(self):
        minimum = optimize.fmin(self.f, 1)

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
        #self.points_ent.insert(0, str(self.S0)+"dBm")
        #self.line0.set_data(*get_data()) # update graph
        #self.line0.set_data(self.t, self.S0)  # update graph
        if self.stokesdrawmode:
            self.line1.set_data(self.t, self.S1)  # update graph
            self.line2.set_data(self.t, self.S2)  # update graph
            self.line3.set_data(self.t, self.S3)  # update graph
        else:
            self.line1.set_data(self.t, self.aziSOP)  # update graph
            self.line2.set_data(self.t, self.ellSOP)  # update graph
            self.line3.set_data(self.t, self.L)  # update graph

        self.DOP_ent.delete(0,"end")
        self.DOP_ent.insert(0,'%6.4f' % self.DOP)
        self.power_ent.delete(0, "end")
        self.power_ent.insert(0, '%6.4f' % self.S0)

        self.graph.set_data(self.S1, self.S2)
        self.graph.set_3d_properties(self.S3)

        self.ellSOP_ent.delete(0,"end")
        self.ellSOP_ent.insert(0, '%6.3f' % (self.avgell*180/np.pi) + u'\u00B0')

        self.aziSOP_ent.delete(0, "end")
        self.aziSOP_ent.insert(0, '%6.3f' % (self.avgazi*180/np.pi) + u'\u00B0')

        self.deltaSOP_ent.delete(0, "end")
        self.deltaSOP_ent.insert(0, '%6.3f' % (self.L.max() *180 /np.pi) + u'\u00B0')
        # self.
        # return self.line0, self.line1, self.line2, self.line3
        return self.line1, self.line2, self.line3, self.graph

    def cal_arclength(self):

        self.aziSOP = np.arctan2(self.S2, self.S1)
        self.ellSOP = np.arctan2(self.S3, np.sqrt(self.S1 ** 2 + self.S2 ** 2))

        b = np.pi / 2 - self.ellSOP[0] * 2
        c = np.pi / 2 - self.ellSOP * 2

        A0 = self.aziSOP[0] * 2
        A1 = self.aziSOP * 2
        A = A1 - A0
        # if A == np.nan:
        #     A = 0

        self.L = np.arccos(np.cos(b) * np.cos(c) + np.sin(b) * np.sin(c) * np.cos(A))


    def get_data2(self):
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
            ndata_show = 2000
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