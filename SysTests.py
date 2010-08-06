import pygst
pygst.require('0.10')
import gst
import alsaaudio
import jack
import os
import time

def setALSA():
    Mixers = [alsaaudio.Mixer(m) for m in alsaaudio.mixers(0)]
    for m in Mixers:
        try: m.setvolume(75)
        except alsaaudio.ALSAAudioError: pass
        try:
            m.getmute()
        except alsaaudio.ALSAAudioError:
            continue
        m.setmute(0)

def testAlsa():
    try:
        mixers = alsaaudio.mixers()
        if not len(mixers) > 1: return False
    except alsaaudio.ALSAAudioError:
        return False
    return True

def testJack():
    unique = str(time.time())
    name = os.path.basename(os.path.basename(__file__))
    
    player = gst.Pipeline("player")
    source = gst.element_factory_make("audiotestsrc", "file-source")
    res = gst.element_factory_make("audioresample", "converter")
    sink = gst.element_factory_make("jackaudiosink", unique)
    player.add(source, res, sink)
    gst.element_link_many(source, res, sink)
    player.set_state(gst.STATE_PAUSED)
    jack.attach(name)
    jack.activate()
    print jack.get_ports()
    print name+":out_"+unique+"_1"
    print name+":out_"+unique+"_1" in jack.get_ports()

    
testJack()
