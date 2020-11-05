from src.main.server.conn.ServerConnection import ServerConnection
from src.main.server.Server import Server
from multiprocessing import Process, SimpleQueue
import os
import json


class Main(object):
    def __init__(self):
        super(Main, self)
        self.gameId = 1
        self.port = 32000
        self.games = {}
        self.sc = ServerConnection(self.port)
        self.sc.startServer()

    def main(self, seed=42):
        self.restoreGames(self.sc)
        self.gameId = self.getNextGameId()
        try:
            while True:
                dc = self.sc.receiveJSON()
                commandType = dc["commandType"]
                if commandType == "newGame":
                    if "seed" in dc:
                        s = dc["seed"]
                    else:
                        s = seed
                    self.initGame(self.gameId, self.sc, dc, s)
                    self.gameId = self.getNextGameId()
                elif commandType == "terminate":
                    idToTerminate = dc["gameId"]
                    if idToTerminate in self.games:
                        self.safeTerminate(dc)
                        #  self.games[idToTerminate]["process"].kill()
                        self.cleanUp()
                elif dc["gameId"] in self.games:
                    self.games[dc["gameId"]]["toProcessQueue"].put(dc)
                else:
                    print("can't find a game with id " + dc["gameId"])

        except KeyboardInterrupt:
            pass
        self.sc.closeServer()

    def safeTerminate(self, dc):
        print("terminating safely")
        gameId = dc["gameId"]
        if dc["terminate"]["fromId"] != self.games[gameId]["admin"]:
            print("terminate didnt come from admin")
            return
        if gameId in self.games:
            self.games[gameId]["process"].kill()
            while not self.games[gameId]["deleteQueue"].empty():
                item = self.games[gameId]["deleteQueue"].get()
                messageId = item["messageId"]
                target = item["target"]
                dc = {"eventType": "message", "message": {"messageId": messageId},
                      "target": target, "mode": "delete", "gameId": gameId}
                self.sc.sendJSON(dc)
            self.cleanUp()

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
                    self.initGame(gameId, sc, dc, s)

    def initGame(self, gameId, sc, dc, seed):
        self.games[gameId] = {"toProcessQueue": SimpleQueue()}
        self.games[gameId]["admin"] = dc["newGame"]["senderId"]
        self.games[gameId]["deleteQueue"] = SimpleQueue()  # dicts with messageId, target
        self.games[gameId]["process"] = \
            Process(target=startNewGame,
                    args=(sc, dc, gameId, self.games[gameId]["toProcessQueue"], seed,
                          self.games[gameId]["deleteQueue"],))
        self.games[gameId]["process"].start()

    def getNextGameId(self):
        self.cleanUp()
        gameId = 0
        while True:
            gameId += 1
            if gameId not in self.games:
                return gameId

    def cleanUp(self):
        remList = []
        for gameId in self.games:
            game: Process = self.games[gameId]["process"]
            if not game.is_alive():
                remList.append(gameId)
        for r in remList:
            print("removing game " + str(r))
            self.games.pop(r, None)
            file = "games/" + str(r) + ".game"
            if os.path.isfile(file):
                os.remove(file)


def startNewGame(sc, dc, gameId, gameQueue, seed, deleteQueue):
    server = Server(seed, sc, dc, gameQueue, gameId, deleteQueue)
    server.start()


if __name__ == "__main__":
    main = Main()
    main.main()
