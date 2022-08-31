import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import matplotlib.animation as animation

import numpy as np
import threading
import tcphandler
import socketserver
import octavethread

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

class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.running = False
        self.ani = None

        btns = tk.Frame(self)
        btns.pack(side=tk.BOTTOM)

        lbl = tk.Label(btns, text="Number of times to run")
        lbl.pack(side=tk.LEFT)

        self.points_ent = tk.Entry(btns, width=5)
        self.points_ent.insert(0, '50')
        self.points_ent.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="update interval (ms)")
        lbl.pack(side=tk.LEFT)

        self.interval = tk.Entry(btns, width=5)
        self.interval.insert(0, '100')
        self.interval.pack(side=tk.LEFT)

        self.btn = tk.Button(btns, text='Start', command=self.on_click)
        self.btn.pack(side=tk.LEFT)

        self.fig = plt.Figure()
        # self.ax0 = self.fig.add_subplot(411)
        # self.ax1 = self.fig.add_subplot(412)
        # self.ax2 = self.fig.add_subplot(413)
        # self.ax3 = self.fig.add_subplot(414)
        # self.line0, = self.ax0.plot([], [], lw=2)
        # self.line1, = self.ax1.plot([], [], lw=2)
        # self.line2, = self.ax2.plot([], [], lw=2)
        # self.line3, = self.ax3.plot([], [], lw=2)

        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312)
        self.ax3 = self.fig.add_subplot(313)

        self.line1, = self.ax1.plot([], [], lw=2)
        self.line2, = self.ax2.plot([], [], lw=2)
        self.line3, = self.ax3.plot([], [], lw=2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # self.maxS = 65535
        # self.minS = 0
        self.maxS = 1
        self.minS = -1
        # self.ax0.set_ylim(0, self.maxS)
        # self.ax0.set_xlim(0, 500)
        self.ax1.set_ylim(self.minS, self.maxS)
        self.ax1.set_xlim(0, 500)
        self.ax2.set_ylim(self.minS, self.maxS)
        self.ax2.set_xlim(0, 500)
        self.ax3.set_ylim(self.minS, self.maxS)
        self.ax3.set_xlim(0, 500)

        # self.S0 = []
        self.S1 = []
        self.S2 = []
        self.S3 = []
        self.t = []
        self.S0 = 0
        self.DOP = 0

    def on_click(self):
        '''the button is a start, pause and unpause button all in one
        this method sorts out which of those actions to take'''
        if self.ani is None:
            # animation is not running; start it
            return self.start()

        if self.running:
            # animation is running; pause it
            self.ani.event_source.stop()
            self.btn.config(text='Un-Pause')
        else:
            # animation is paused; unpause it
            self.ani.event_source.start()
            self.btn.config(text='Pause')
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
        self.btn.config(text='Pause')
        self.ani._start()
        print('started animation')

    def update_graph(self, i):
        self.get_data()
        #self.points_ent.insert(0, str(self.S0)+"dBm")
        #self.line0.set_data(*get_data()) # update graph
        #self.line0.set_data(self.t, self.S0)  # update graph
        self.line1.set_data(self.t, self.S1)  # update graph
        self.line2.set_data(self.t, self.S2)  # update graph
        self.line3.set_data(self.t, self.S3)  # update graph

        # return self.line0, self.line1, self.line2, self.line3
        return self.line1, self.line2, self.line3

    def get_data(self):
        '''replace this function with whatever you want to provide the data
        for now, we just return soem random data'''
        # rand_x = list(range(100))
        # rand_y = [random.randrange(100) for _ in range(100)]
        # return rand_x, rand_y
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
            tDOP = tmpdata[:, -2]
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