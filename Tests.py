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
            if not os.path.exists(filename): raise IOError
            self.player.set_property("uri", "file://" + filename)
            self.player.set_state(gst.STATE_PAUSED)
        except Exception, e:
            self.statuses['GST'] = e
            
    def Jack(self):
        try:
            jack.attach(self.name)
            jack.activate()
        except Exception, e:
            self.statuses['Jack'] = e
    
    def Connect(self):
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
            self.statuses['Connect'] = e

    def Play(self):
        try:
            self.player.set_state(gst.STATE_PLAYING)
            time.sleep(1)
        except Exception, e:
            self.statuses['Play'] = e
    
    def cleanup(self):
        jack.detach()

    def run(self):
        self.Jack()
        self.GST()
        self.Connect()
        self.Play()
        print self.statuses
    
a = Tester()
a.run()