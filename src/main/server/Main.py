from src.main.server.conn.ServerConnection import ServerConnection
from src.main.server.Server import Server
import threading
from queue import SimpleQueue


class Main(object):
    def __init__(self):
        super(Main, self)
        self.gameId = 1
        self.gameQueues = {}
        self.port = 32000

    def main(self, seed=42):
        sc = ServerConnection(self.port)
        sc.startServer()
        try:
            while True:
                dc = sc.receiveJSON()
                commandType = dc["commandType"]
                if commandType == "newGame":
                    self.gameQueues[self.gameId] = SimpleQueue()
                    threading.Thread(target=startNewGame,
                                     args=(sc, dc, self.gameId,
                                           self.gameQueues[self.gameId],)).start()
                    self.gameId += 1
                elif dc["gameId"] in self.gameQueues:
                    self.gameQueues["gameId"].put(dc)
                else:
                    print("can't find a game with id " + dc["gameId"])

        except KeyboardInterrupt:
            pass
        sc.closeServer()


def startNewGame(sc, dc, gameId, gameQueue):
    server = Server(sc, dc["newGame"]["senderId"], dc["origin"], gameQueue, gameId)
    server.start()


if __name__ == "__main__":
    main = Main()
    main.main()
