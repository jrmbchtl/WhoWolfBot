from src.main.client.conn.ServerConnection import ServerConnection


class Systemtest(object):
    def __init__(self, sc):
        super(Systemtest, self)
        self.sc: ServerConnection = sc

    def run(self):
        pass

    def asserReceiveDict(self, dc):
        rec = self.sc.receiveJSON()
        self.dictCompare(rec, dc)

    def dictCompare(self, dc1, dc2):
        for key in dc1:
            assert key in dc2
            assert dc1[key] == dc2[key]
        for key in dc2:
            assert key in dc1
            assert dc2[key] == dc1[key]
