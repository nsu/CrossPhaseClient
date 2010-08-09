import Tests
import ConfigParser


class shake(object):
    def __init__(self, data):
        self.tester = Tests.Tester()
        self.confParser = ConfigParser.RawConfigParser()
        self.retVal = {'TYPE':'SHAKE'}
    
    def run(self):
        self.retVal['TESTS'] = self.tester.run()
        fp = open('crossPhase.conf', 'r')
        self.confParser.readfp(fp)
        fp.close()
        self.retVal['CHANS'] = self.confParser.get('hardware', 'channels')
        return self.retVal