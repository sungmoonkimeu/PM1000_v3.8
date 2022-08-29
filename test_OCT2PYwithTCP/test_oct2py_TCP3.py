import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np
import threading
import tcphandler
import socketserver
import octavethread

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

def dataclear():
    received_data.clear()

# Start the threads
othread = octavethread.OctaveThread()
sthread = ServerThread()

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

plt.axes(xlim=(0, 500), ylim=(0, 65535))
fig = plt.Figure(dpi=100)
ax = fig.add_subplot(121, xlim=(0, 500), ylim=(0, 65535))
#ax2 = fig.add_subplot(233, projection='3d', xlim=(0, 500), ylim=(0, 65535))  # polar subplot
ax2 = fig.add_subplot(122, xlim=(0, 500), ylim=(0, 65535))
# Keep updating the drawing
S0, S1, S2, S3 = [], [], [], []
xx = np.arange(0,500,1)
yy = xx*0
(ln0, ) = ax.plot(xx, yy)
(ln1, ) = ax.plot(xx, yy)
(ln2, ) = ax.plot(xx, yy)
(ln3, ) = ax.plot(xx, yy)

(ln20, ) = ax2.plot(xx, yy)
(ln21, ) = ax2.plot(xx, yy)
(ln22, ) = ax2.plot(xx, yy)
(ln23, ) = ax2.plot(xx, yy)

# plt.show(block=False)
# plt.pause(0.1)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

# canvas = FigureCanvasTkAgg(fig2, master=root)
# canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

#button = tkinter.Button(master=root, text="Quit", command=root.quit)
button = tkinter.Button(master=root, text="Quit", command=root.destroy)
button.pack(side=tkinter.BOTTOM)

# runbutton = tkinter.Button(root, text='Run animation', command = runanimation)
# runbutton.pack(side=tkinter.BOTTOM)

toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def animate(i, S0, S1, S2, S3):
    data_available.wait()
    # anim = animation.FuncAnimation(fig, animate, init_func=init,frames=200, interval=20, blit=True)
    tmpdata = np.array(received_data)  # ~1ms
    # print(tmpdata.size)
    ndata = 32 * 10
    if tmpdata.size > ndata * 4:  # ~1ms
        # print("comecome")
        tS0 = tmpdata[:, 0:ndata - 1]
        S0 = np.hstack((S0, tS0.reshape(tS0.size)))
        tS1 = tmpdata[:, ndata:ndata * 2 - 1]
        S1 = np.hstack((S1, tS1.reshape(tS1.size)))
        tS2 = tmpdata[:, ndata * 2:ndata * 3 - 1]
        S2 = np.hstack((S2, tS2.reshape(tS2.size)))
        tS3 = tmpdata[:, ndata * 3:ndata * 4 - 1]
        S3 = np.hstack((S3, tS3.reshape(tS3.size)))

        # now = time.time()
        # print("Elapsed %f" % (time.time() - now))
        ndata_show = 500
        nstep = 1
        S0 = S0[-ndata_show::nstep]
        S1 = S1[-ndata_show::nstep]
        S2 = S2[-ndata_show::nstep]
        S3 = S3[-ndata_show::nstep]

        t = np.arange(0, len(S0), 1)
        ln0.set_data(t, S0)
        ln1.set_data(t, S1)
        ln2.set_data(t, S2)
        ln3.set_data(t, S3)

        t = np.arange(0, len(S0), 1)
        ln20.set_data(t, S0)
        ln21.set_data(t, S1)
        ln22.set_data(t, S2)
        ln23.set_data(t, S3)


        dataclear()
    data_available.clear()
    return ln0, ln1, ln2, ln3, ln20, ln21, ln22, ln23


anim = animation.FuncAnimation(fig, animate, fargs=(S0, S1, S2, S3), interval= 5, blit=True)
# anim2 = animation.FuncAnimation(fig2, animate2, fargs=(S0, S1, S2, S3), interval= 5, blit=True)

tkinter.mainloop()