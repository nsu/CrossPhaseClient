class cueList(object):
    def __init__(self, id, eTime, commands, exe):
        self.player = exe.handler.server.getPlayer(id)