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
    basename = os.path.abspath('.')
    filename = basename+'/testNoise.mp3'
    if not os.path.exists(filename): raise IOError
    player.set_property("uri", "file://" + filename)
    player.set_state(gst.STATE_PAUSED)
    return player


def makeJack(unique):
    selfName = os.path.basename(os.path.basename(__file__))
    time.sleep(.1)
    jack.attach(selfName)
    jack.activate()
    systemPorts = set(jack.get_ports())
    if not selfName+":out_"+unique+"_1" in jack.get_ports(): return False
    return True

def makeConnect(unique):
    allPorts = jack.get_ports()
    selfPort = [port for port in allPorts if unique in port][0]
    inPorts = [port for port in allPorts if 'playback' in port]
    try:
        for port in inPorts:
            jack.connect(selfPort, port)
    except:
        return False
    return True

def makeGo(player):
    player.set_state(gst.STATE_PLAYING)
    time.sleep(5)
    return True

def runTest():
    unique = str(time.time())
    player = makeGST(unique)
    print "GST Status: ", bool(player)
    print "Jack Status: ", makeJack(unique)
    print "Connect Status: ", makeConnect(unique)
    print "Go status: ", makeGo(player)

runTest()
