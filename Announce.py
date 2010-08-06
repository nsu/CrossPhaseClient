from AvahiInterface import Zeroconf
import time, os, threading

class Announcer(object):
    def __init__(self):
        ip = os.popen('ifconfig eth0').readlines()[1].split()[1].split(':')[1]
        self.service = Zeroconf(name="ATS0", port=3141, stype="_ats._tcp", host="%s.local." %ip)
        
    def pub(self):
            self.service.publish()

    def unpub(self):
        self.service.unpublish()
        