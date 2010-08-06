import pygst
pygst.require('0.10')
import gst
import alsaaudio
import jack
import os
import time



def makeGST(unique):
    unique=unique
    player = gst.element_factory_make("playbin2", "player")
    fakesink = gst.element_factory_make("fakesink", "fakesink")
    jacksink = gst.element_factory_make("jackaudiosink", unique)
    jacksink.set_property('connect', 'none')
    player.set_property("video-sink",  fakesink)
    player.set_property("audio-sink",  jacksink)
    filename = '/home/n/Code/CrossPhase/testNoise.mp3'
    if not os.path.exists(filename): raise IOError
    player.set_property("uri", "file://" + filename)
    player.set_state(gst.STATE_PAUSED)
    return True


def makeJack(unique):
    selfName = os.path.basename(os.path.basename(__file__))
    time.sleep(.1)
    jack.attach(selfName)
    jack.activate()
    systemPorts = set(jack.get_ports())
    if not selfName+":out_"+unique+"_1" in jack.get_ports(): return False
    print [input for input in systemPorts if ":playback" in input]
    
    return True

def runTest():
    unique = str(time.time())
    makeGST(unique)
    makeJack(unique)

runTest()