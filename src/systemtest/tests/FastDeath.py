from src.systemtest.Systemtest import Systemtest


class FastDeath(Systemtest):

    def run(self):
        gameId = self.initGame()

        print(gameId)
