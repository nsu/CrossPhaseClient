import ConfigParser
import time

import Tests
import Player
import jack


class base(object):
    def __init__(self, data, handler):
        self.retVal = {'TYPE':data['TYPE']}
        self.handler = handler
        
    def addVal(self, key, val):
        self.retVal[key.upper()]=val

class shake(base):
    def __init__(self, data, handler):
        base.__init__(self, data, handler)
        self.tester = Tests.Tester()
        self.confParser = ConfigParser.RawConfigParser()
    
    def getChans(self):
        fp = open('crossPhase.conf', 'r')
        self.confParser.readfp(fp)
        fp.close()
        return self.confParser.get('system', 'channels')
    
    def run(self):
        results = self.tester.run()
        chans = self.getChans()
        self.addVal('tests', results)
        self.addVal('chans', chans)
        return self.retVal

class makeplayer(base):
    def add():
        pass
            
    def run(self):
        player = Player.Player(self.handler.name)
        self.addVal('uuid', player.getUUID())
        return self.retVal