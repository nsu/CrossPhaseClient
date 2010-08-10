import pygst
pygst.require('0.10')
import gst

import time
import os
import jack
import random

import uuid

import time

class Player():
    def __init__(self, name):
        self.name = name
        self.uuid=str(uuid.uuid4())
        self.player = gst.element_factory_make("playbin2", "player"+self.uuid)
        self.fakesink = gst.element_factory_make("fakesink", "fakesink"+self.uuid)
        self.jacksink = gst.element_factory_make("jackaudiosink", "jsink"+self.uuid)
        self.jacksink.set_property('connect', 'none')
        self.player.set_property("video-sink", self.fakesink)
        self.player.set_property("audio-sink", self.jacksink)        

    def getUUID(self):
        return self.uuid

    def setPath(self, filepath):
        self.player.set_property("uri", "file://" + filepath)

    def prepare(self):
        self.player.set_state(gst.STATE_PAUSED)
        time.sleep(.1)
    
    def jConnect(self, output, input):
        output, input = str(output), str(input)
        print self.name+":out_jsink"+self.uuid+"_"+output,"alsa_pcm:playback_"+input
        jack.connect(self.name+":out_jsink"+self.uuid+"_"+output,"alsa_pcm:playback_"+input)

    def jDConnect(self, output, input):
        output, input = str(output), str(input)
        os.system("jack_disconnect "+self.name+":out_jsink"+self.uuid+"_"+output+" alsa_pcm:playback_"+input)
        
    def play(self):
        self.player.set_state(gst.STATE_PLAYING)

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)
    
    def getVolume(self):
        return self.player.get_property("volume")

    def setVolume(self, vol):
        self.player.set_property("volume", vol)
    
    def getPos(self):
        return self.player.query_position(gst.FORMAT_TIME, None)[0]/1000000000
        
    def fadeRel(self, vol, secs):
        t = time.time()
        delta = vol/float((secs*100))
        final = self.getVolume()+vol
        for i in xrange(secs*100):
            self.setVolume(self.getVolume()+delta)
            # print self.getVolume()
            time.sleep(.01)
        self.setVolume(final)
        print self.getVolume()
        # print "LASTED: " + str(time.time()-t)
    
    def fadeAbs(self, vol, secs):
        print self.player.get_property("uri")
        self.fadeRel(vol-self.getVolume(), secs)
    
    def seekRel(self, secs):
        pos_int = self.player.query_position(gst.FORMAT_TIME, None)[0]
        seek_ns = pos_int + (secs * 1000000000)
        self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek_ns)

    def seekAbs(self, secs):
        seek_ns = secs * 1000000000
        self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek_ns)