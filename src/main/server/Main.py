from src.main.server.conn.ServerConnection import ServerConnection
from src.main.server.Server import Server
from multiprocessing import Process, SimpleQueue


class Main(object):
    def __init__(self):
        super(Main, self)
        self.gameId = 1
        self.gameQueues = {}
        self.port = 32000
        self.runningGames = {}

    def main(self, seed=42):
        sc = ServerConnection(self.port)
        sc.startServer()
        try:
            while True:
                dc = sc.receiveJSON()
                commandType = dc["commandType"]
                if commandType == "newGame":
                    self.gameQueues[self.gameId] = SimpleQueue()
                    self.runningGames[self.gameId] = \
                        Process(target=startNewGame, args=(sc, dc, self.gameId,
                                                           self.gameQueues[self.gameId], seed,))
                    self.runningGames[self.gameId].start()
                    self.gameId += 1
                elif commandType == "terminate":
                    idToTerminate = dc["gameId"]
                    if idToTerminate in self.runningGames:
                        self.runningGames[idToTerminate].kill()
                elif dc["gameId"] in self.gameQueues:
                    self.gameQueues[dc["gameId"]].put(dc)
                else:
                    print("can't find a game with id " + dc["gameId"])

        except KeyboardInterrupt:
            pass
        sc.closeServer()


def startNewGame(sc, dc, gameId, gameQueue, seed):
    server = Server(seed, sc, dc["newGame"]["senderId"], dc["origin"], gameQueue, gameId)
    server.start()


if __name__ == "__main__":
    main = Main()
    main.main()
