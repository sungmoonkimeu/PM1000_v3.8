# Filename tcphandler.py
import socketserver
import json

class MyTCPHandler(socketserver.BaseRequestHandler):
    callback = None

    """
    The RequestHandler class for our server.
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        data = bytearray()
        datachunk = self.request.recv(1024)
        while datachunk:
            # glue the chunks together, alternatively use larger buffer
            data.extend(datachunk)
            datachunk = self.request.recv(1024)
        if MyTCPHandler.callback is not None and len(data) > 0:
            MyTCPHandler.callback(json.loads(data))
