from .Systemtest import Systemtest


class Exampletest(Systemtest):

    def run(self):
        print("running Exampletest")
        self.sc.sendJSON({"commandType": "newGame", "newGame": {"senderId": 42}, "origin": 1})
        self.asserReceiveDict({"eventType": "gameStarted", "gameId": 1})
