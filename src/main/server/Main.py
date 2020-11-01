from src.main.server.conn.ServerConnection import ServerConnection
from src.main.server.Server import Server
from multiprocessing import Process, SimpleQueue
import os
import json


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
        self.restoreGames(sc)
        self.gameId = self.getNextGameId()
        try:
            while True:
                dc = sc.receiveJSON()
                commandType = dc["commandType"]
                if commandType == "newGame":
                    if "seed" in dc:
                        s = dc["seed"]
                    else:
                        s = seed
                    self.gameQueues[self.gameId] = SimpleQueue()
                    self.runningGames[self.gameId] = \
                        Process(target=startNewGame, args=(sc, dc, self.gameId,
                                                           self.gameQueues[self.gameId], s,))
                    self.runningGames[self.gameId].start()
                    self.gameId = self.getNextGameId()
                elif commandType == "terminate":
                    idToTerminate = dc["gameId"]
                    if idToTerminate in self.runningGames:
                        self.runningGames[idToTerminate].kill()
                        self.cleanUp()
                elif dc["gameId"] in self.gameQueues:
                    self.gameQueues[dc["gameId"]].put(dc)
                else:
                    print("can't find a game with id " + dc["gameId"])

        except KeyboardInterrupt:
            pass
        sc.closeServer()

    def restoreGames(self, sc):
        if not os.path.isdir("games/"):
            os.mkdir("games/")
        else:
            files = os.listdir("games/")
            for f in files:
                if not os.path.isfile("games/" + f):
                    continue
                if f.endswith(".game"):
                    try:
                        gameId = int(f.split(".")[0])
                    except ValueError:
                        continue
                    with open("games/" + f) as json_file:
                        data = json.load(json_file)
                    admin = data["admin"]
                    chatId = data["chatId"]
                    s = data["seed"]
                    numberSent = data["numberSent"]
                    recList = data["recList"]
                    dc = {"commandType": "newGame", "newGame":
                        {"senderId": admin, "numberSent": numberSent, "recList": recList},
                        "origin": chatId}
                    self.gameQueues[gameId] = SimpleQueue()
                    self.runningGames[gameId] = \
                        Process(target=startNewGame, args=(sc, dc, gameId,
                                                           self.gameQueues[gameId], s,))
                    self.runningGames[gameId].start()

    def getNextGameId(self):
        self.cleanUp()
        gameId = 0
        while True:
            gameId += 1
            if gameId not in self.runningGames:
                return gameId

    def cleanUp(self):
        remList = []
        for gameId in self.runningGames:
            game: Process = self.runningGames[gameId]
            if not game.is_alive():
                remList.append(gameId)
        for r in remList:
            print("removing game " + str(r))
            self.runningGames.pop(r, None)
            self.gameQueues.pop(r, None)
            file = "games/" + str(r) + ".game"
            if os.path.isfile(file):
                os.remove(file)


def startNewGame(sc, dc, gameId, gameQueue, seed):
    server = Server(seed, sc, dc, gameQueue, gameId)
    server.start()


if __name__ == "__main__":
    main = Main()
    main.main()
