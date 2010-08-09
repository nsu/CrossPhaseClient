import socket
import threading
import SocketServer
import json
import os
from time import sleep
import jack

import Execs
import Player
import Cue

class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):
    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.opts = {}
        self.opts['SHAKE']=Execs.shake
                
    def handle(self):
        raw = self.rfile.readline()
        try:
            data = json.loads(raw)
        except ValueError, e:
            self.wfile.write("{'TYPE':'ERROR': 'Could not load packet to JSON: %s}" % raw.rstrip())
            return False
        self.wfile.write("%s\n" % self.opts[data['TYPE']](data).run())
        return True
        
        
        

    def cleanup(self):
        pass
        
            
        
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    def __init__(self, hpTuple, handler):
        SocketServer.TCPServer.__init__(self, hpTuple, handler)
        self.name = name = os.path.basename(__file__)
        jack.attach(name)
        jack.activate()
        self.allOutputs = set([output for output in jack.get_ports() if 'playback' in output])
        self.ownedOutputs = set()
        print self.allOutputs


if __name__ == "__main__":
    
    HOST, PORT = "", 3141 
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    print os.getpid()

    server_thread.setDaemon(True)
    server_thread.start()
    print "Server Initiated"
    while True:
        sleep(25)

