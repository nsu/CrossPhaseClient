import socket
import threading
import SocketServer
import json
import os
from time import sleep
import jack

import Player

class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):
    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.opts = {}
        # self.opts['SHAKE']=
                
    def handle(self):
        p = Player.Player(0, os.path.basename(__file__))
        p.setPath("/home/n/Code/audiodist/04.mp3")
        # sleep(1)
        p.prepare()
        p.jConnect(1,1)
        p.jConnect(2,1)
        p.play()
        sleep(3 )
        p.jDConnect(1,1)
        p.jConnect(1,2)
        p.jDConnect(2,1)
        p.jConnect(2,2)
        p.play()
        sleep(30)
        
    def cleanup(self):
        pass
        
            
        
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    def __init__(self, hpTuple, handler):
        SocketServer.TCPServer.__init__(self, hpTuple, handler)
        self.allOutputs = set([output for output in jack.get_ports() if 'playback' in output])
        self.ownedOutputs = set()
        print self.allOutputs


if __name__ == "__main__":
    name = os.path.basename(__file__)
    jack.attach(name)
    jack.activate()
    
    HOST, PORT = "", 3141 
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    print os.getpid()

    server_thread.setDaemon(True)
    server_thread.start()
    print "Server Initiated"
    while True:
        sleep(25)

