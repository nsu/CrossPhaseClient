import threading
import time

class cueList(object):
    def __init__(self, id, eTime, commands, exe):
        self.exe = exe
        self.player = exe.handler.server.getPlayer(id)
        self.eTime = eTime
        self.commands = commands
        self.cList = {}
        self.cList['SETPATH'] = self.setPath
        self.cList['GETPATH'] = self.getPath
        self.cList['PLAY'] = self.play
        self.cList['PAUSE'] = self.pause
        self.cList['STOP'] = self.stop
        self.cList['SETVOLUME'] = self.setVolume
        self.cList['GETVOLUME'] = self.getVolume
        self.cList['FADEREL'] = self.fadeRel
        self.cList['FADEABS'] = self.fadeAbs
        self.cList['SEEKREL'] = self.seekRel
        self.cList['SEEKABS'] = self.seekAbs
        self.cList['DELETE'] = self.destroy
        self.cList['CONNECT'] = self.connect
    
    def startTimer(self):
         if self.eTime: 
             timediff = self.eTime - time.time()
             print timediff
             time.sleep(timediff)
         self.run()
         
    
    def run(self):
        for command in self.commands:
            print command['ACTION']
            time.sleep(command['SLEEP'])
            self.cList[command['ACTION']](command['ARGS'])
            
    def setPath(self, args):
        self.player.setPath(args[0])
    
    def getPath(self, args):
        print self.player.getPath()
    
    def play(self, args):
        self.player.prepare()
        self.player.play()
    
    def pause(self, args):
        self.player.pause()
    
    def stop(self, args):
        self.player.stop()
    
    def setVolume(self, args):
        self.player.setVolume(args[0])

    def getVolume(self, args):
        return self.player.getVolume()
        
    def fadeRel(self, args):
        self.player.fadeRel(args[0], args[1])

    def fadeAbs(self, args):
        self.player.fadeAbs(args[0], args[1])

    def seekRel(self, args):
        self.player.seekRel(args[0])

    def seekAbs(self, args):
        self.player.seekAbs(args[0])

    def destroy(self, args):
        self.player.die()
        self.exe.handler.server.delPlayer(self.player.getUUID())
        del(self.player)

    def connect(self, args):
        self.player.jConnect(args[0], args[1])
        
    def disconnect(self, args):
        self.player.jDConnect(args[0], args[1])
    
    def delete(self, args):
        self.player.die()