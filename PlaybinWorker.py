import pygst
pygst.require('0.10')
import gst

import time
import os
import jack
import random

import time, random

class Player():
    def __init__(self, num):
        self.num=num
        self.player = gst.element_factory_make("playbin2", "player"+num)
        self.fakesink = gst.element_factory_make("fakesink", "fakesink"+num)
        self.jacksink = gst.element_factory_make("jackaudiosink", "jsink"+num)
        self.player.set_property("video-sink", self.fakesink)
        self.player.set_property("audio-sink", self.jacksink)

    def setPath(self, filepath):
        self.player.set_property("uri", "file://" + filepath)

    def prepare(self):
        self.player.set_state(gst.STATE_PAUSED)
    
    def play(self):
        self.player.set_state(gst.STATE_PLAYING)
        
    def getVolume(self):
        return self.player.get_property("volume")
    
    def setVolume(self, vol):
        self.player.set_property("volume", vol)

p = Player("0")
p.setPath("/home/n/Code/audiodist/04.mp3")

time.sleep(.1)

q = Player("1")
q.setPath("/home/n/Code/audiodist/5.mp3")

time.sleep(.1)

r = Player("2")
r.setPath("/home/n/Code/audiodist/audiodump.m4a")


q.prepare()
p.prepare()
r.prepare()

time.sleep(.1)

jack.attach("PlaybinWorker.py")
jack.activate()

jack.connect("PlaybinWorker.py:out_jsink0_1","alsa_pcm:playback_5")
jack.disconnect("PlaybinWorker.py:out_jsink0_1","alsa_pcm:playback_5")
jack.connect("PlaybinWorker.py:out_jsink0_2","alsa_pcm:playback_6")
# 
# jack.connect("PlaybinWorker.py:out_jsink1_1","alsa_pcm:playback_5")
# jack.connect("PlaybinWorker.py:out_jsink1_2","alsa_pcm:playback_6")
# 
# jack.connect("PlaybinWorker.py:out_jsink2_1","alsa_pcm:playback_5")
# jack.connect("PlaybinWorker.py:out_jsink2_2","alsa_pcm:playback_6")

p.play()
p.setVolume(0)
for i in xrange(50):
    p.setVolume(p.getVolume()+.02)
    time.sleep(.1)
for i in xrange(50):
    p.setVolume(p.getVolume()-.01)
    time.sleep(.1) 
q.setVolume(0)
q.play()
for i in xrange(50):
    p.setVolume(p.getVolume()-.01)
    q.setVolume(q.getVolume()+.01)
    time.sleep(.1)
for i in xrange(50):
    q.setVolume(q.getVolume()+.01)
    time.sleep(.1)
r.setVolume(0)
r.play()
for i in xrange(100):
    q.setVolume(q.getVolume()-.01)
    r.setVolume(r.getVolume()+.01)
    time.sleep(.1)
for i in xrange(100):
    r.setVolume(r.getVolume()-.01)
    time.sleep(.1)


time.sleep(120)