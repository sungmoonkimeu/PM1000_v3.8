# This is the main script to run
import threading
import tcphandler
import socketserver
import octavethread
from matplotlib import pyplot as plt
import numpy as np
import time

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

# Keep updating the drawing
S0, S1, S2, S3 = [], [], [], []

fig, ax = plt.subplots()
ax.set(xlim=(0, 500), ylim=(0, 65535))
t = []
xx = np.arange(0,500,1)
yy = xx*0
(ln0, ) = ax.plot(xx, yy, animated=True)
(ln1, ) = ax.plot(xx, yy, animated=True)
(ln2, ) = ax.plot(xx, yy, animated=True)
(ln3, ) = ax.plot(xx, yy, animated=True)
plt.show(block=False)
plt.pause(0.1)
bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(ln0)
ax.draw_artist(ln1)
ax.draw_artist(ln2)
ax.draw_artist(ln3)
fig.canvas.blit(fig.bbox)
while True:
    #Wait forever until new data_available event is raised
    data_available.wait()
    # Plot the latest data-set received.

    tmpdata = np.array(received_data)  # ~1ms
    #print(tmpdata.size)
    ndata = 32 * 10
    if tmpdata.size > ndata * 4:  # ~1ms
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

        t = np.arange(0,len(S0),1)
        #plt.plot(received_data[len(received_data)-1] )

        # now = time.time()
        # fig.canvas.restore_region(bg)
        ln0.set_ydata(S0)
        ln1.set_ydata(S1)
        ln2.set_ydata(S2)
        ln3.set_ydata(S3)
        ax.draw_artist(ln0)
        ax.draw_artist(ln1)
        ax.draw_artist(ln2)
        ax.draw_artist(ln3)
        fig.canvas.blit(fig.bbox)

        fig.canvas.flush_events()

        dataclear()
        plt.pause(0.0001)

    data_available.clear()



