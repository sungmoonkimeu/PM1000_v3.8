# This is the main script to run
import threading
import tcphandler
import socketserver
import octavethread
from matplotlib import pyplot as plt
import numpy as np

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

# Start the threads
othread = octavethread.OctaveThread()
sthread = ServerThread()

# Keep updating the drawing
S0, S1, S2, S3 = [], [], [], []
while True:
    #Wait forever until new data_available event is raised
    data_available.wait()
    # Plot the latest data-set received.
    # print(np.array(received_data).shape)
    # S0 = np.hstack((S0, received_data[-1][0:127]))
    # S1 = np.hstack((S1, received_data[-1][128:128*2-1]))
    # S2 = np.hstack((S2, received_data[-1][128*2:128*3-1]))
    # S3 = np.hstack((S3, received_data[-1][128*3:128*4-1]))
    tmpdata = np.array(received_data)
    print(tmpdata.size)
    ndata = 128*100
    S0 = tmpdata[:, 0:ndata-1]
    S0 = S0.reshape(S0.size)
    S1 = tmpdata[:, ndata:ndata*2-1]
    S1 = S1.reshape(S1.size)
    S2 = tmpdata[:, ndata*2:ndata*3-1]
    S2 = S2.reshape(S2.size)
    S3 = tmpdata[:, ndata * 3:ndata * 4 - 1]
    S3 = S3.reshape(S3.size)

    S0 = S0[-100000:]
    S1 = S1[-100000:]
    S2 = S2[-100000:]
    S3 = S3[-100000:]


    t = np.arange(0,len(S0),1)
    #plt.plot(received_data[len(received_data)-1] )
    plt.plot(t,S0,t,S1,t,S2,t,S3)
    # For some reason this works to have an animated-like drawing
    plt.draw()
    plt.pause(0.0001)
    plt.clf()
    # clear the event
    data_available.clear()
