import pygst
pygst.require('0.10')
import gst
import alsaaudio
import jack
import os
import time


class Tester(object):
    def __init__(self):
        self.unique = str(time.time())
        self.statuses = {}
        self.name = os.path.basename(__file__)
    
    def GST(self):
        try:
            self.player = gst.element_factory_make("playbin2", "self.player")
            fakesink = gst.element_factory_make("fakesink", "fakesink")
            jacksink = gst.element_factory_make("jackaudiosink", self.unique)
            jacksink.set_property('connect', 'none')
            self.player.set_property("video-sink",  fakesink)
            self.player.set_property("audio-sink",  jacksink)
            basename = os.path.abspath('.')
            filename = basename+'/testNoise.mp3'
            if not os.path.exists(filename): raise IOError("Could not find test file")
            self.player.set_property("uri", "file://" + filename)
            self.player.set_state(gst.STATE_PAUSED)
        except Exception, e:
            self.statuses['GST'] = e            
    
    def Jack(self):
        try:
            for i in xrange(10):
                selfPort = [port for port in jack.get_ports() if self.unique in port]
                if not selfPort: time.sleep(.01)
                else: break
            if not selfPort: raise jack.UsageError("Test port could not be registered", "Try increasing sleep time")
            allPorts = jack.get_ports()
            selfPort = [port for port in allPorts if self.unique in port][0]
            inPorts = [port for port in allPorts if 'playback' in port]
            for port in inPorts:
                jack.connect(selfPort, port)
        except Exception, e:
            self.statuses['Jack'] = e

    def Play(self):
        try:
            self.player.set_state(gst.STATE_PLAYING)
            # time.sleep(1)
        except Exception, e:
            self.statuses['Play'] = e
        
    def ALSA(self):
        try:
            Mixers = [alsaaudio.Mixer(m) for m in alsaaudio.mixers(0)]
            if len(Mixers) < 1: raise alsaaudio.ALSAAudioError
        except:
            self.statuses['ALSA'] = "Something has gone terribly wrong with ALSA"

    def cleanup(self):
        self.player.set_state(gst.STATE_NULL)

    def run(self):
        self.ALSA()
        self.GST()
        self.Jack()
        self.Play()
        self.cleanup()
        return self.statuses
    
if __name__ == '__main__':
    t = Tester()
    t.run() 
