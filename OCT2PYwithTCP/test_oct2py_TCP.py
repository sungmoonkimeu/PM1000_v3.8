# This is the main script to run
import threading
import tcphandler
import socketserver
import octavethread
from matplotlib import pyplot as plt

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
while True:
    #Wait forever until new data_available event is raised
    data_available.wait()
    # Plot the latest data-set received.
    plt.plot(received_data[len(received_data)-1] )
    # For some reason this works to have an animated-like drawing
    plt.draw()
    plt.pause(0.0001)
    plt.clf()
    # clear the event
    data_available.clear()
