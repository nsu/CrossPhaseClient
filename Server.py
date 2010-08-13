import socket
import threading
import SocketServer
import json
import os
from time import sleep

import Execs

class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):
    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.opts = {}
        self.opts['SHAKE']=Execs.shake
        self.opts['MAKEPLAYER']=Execs.makeplayer
        self.opts['EXEC']=Execs.execute
                
    def handle(self):
        raw = self.rfile.readline()
        print raw
        try:
            data = json.loads(raw)
        except ValueError, e:
            self.wfile.write(json.dumps({'TYPE':'ERROR', 'MESSAGE': 'Could not load packet to JSON: %s' % raw.rstrip()}))
            return False
        self.wfile.write("%s\n" % json.dumps(self.opts[data['TYPE']](data, self).run()))
        return True
                
    def cleanup(self):
        pass
        
            
        
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    def __init__(self, hpTuple, handler):
        SocketServer.TCPServer.__init__(self, hpTuple, handler)
        self.name = os.path.basename(__file__)
        self.players = {}
        print "Server Initiated"
        
    def addPlayer(self, id, player):
        self.players[id] = player
    
    def getPlayer(self, id):
        return self.players[id]
    
    def delPlayer(self, id):
        del(self.players[id])

if __name__ == "__main__":
    
    HOST, PORT = "", 3141 
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.setDaemon(True)
    server_thread.start()
    while True:
        sleep(25)

