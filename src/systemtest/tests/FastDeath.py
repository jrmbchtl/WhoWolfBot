from src.systemtest.Systemtest import Systemtest


class FastDeath(Systemtest):

    def getName(self):
        return "FastDeath"

    def run(self):
        gameId = self.initGame()
        print(gameId)
