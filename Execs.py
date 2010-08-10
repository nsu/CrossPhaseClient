import ConfigParser
import time

import Tests
import Player
import Cue



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
        chans = self.getChans()
        self.addVal('chans', chans)
        results = self.tester.run()
        self.addVal('tests', results)
        return self.retVal

class makeplayer(base):
    def run(self):
        player = Player.Player(self.handler.server.name)
        uuid = player.getUUID()
        self.addVal('PLAYERID', uuid)
        self.handler.server.addPlayer(uuid, player)
        return self.retVal

class buildcue(base):
    def __init__(self, data, handler):
        base.__init__(self, data, handler)
        self.data = data
    
    
    def run(self):
        new = Cue.cueList(id=self.data['PLAYERID'],
            eTime=self.data['EXECTIME'],
            commands=self.data['COMMANDS'],
            exe=self
        )
        