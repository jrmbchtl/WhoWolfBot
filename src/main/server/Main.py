import argparse
import sys
import os
import json
from multiprocessing import Process, SimpleQueue

from src.main.client.TelegramClient import TelegramClient
from src.main.server import Factory
from src.main.server.conn.ServerConnection import ServerConnection
from src.main.server.Server import Server
from src.systemtest.SystemTestMain import SystemTestMain
from src.main.localization import getLocalization as loc

lang = "EN"


class Main(object):
    def __init__(self, enableTclient=False, enableSysTestClient=False):
        super(Main, self)
        self.gameId = 1
        self.port = 32000
        self.games = {}
        self.fromServerQueue = SimpleQueue()
        self.toServerQueue = SimpleQueue()
        self.sc = ServerConnection(self.toServerQueue, self.fromServerQueue)
        self.clientList = []
        if enableTclient:
            self.clientList.append(Process(target=startTelegramClient,
                                           args=(self.fromServerQueue, self.toServerQueue,)))
            self.clientList[len(self.clientList) - 1].start()
        if enableSysTestClient:
            self.clientList.append(Process(target=startTesting,
                                           args=(self.fromServerQueue, self.toServerQueue,)))
            self.clientList[len(self.clientList) - 1].start()

    def main(self, seed=42):
        self.restoreGames(self.sc)
        self.gameId = self.getNextGameId()
        try:
            self.gameLoop(seed)
        except KeyboardInterrupt:
            self.closeServer()

    def gameLoop(self, seed):
        while True:
            dc = self.sc.receiveJSON()
            commandType = dc["commandType"]
            if commandType == "newGame":
                if "seed" in dc["newGame"]:
                    s = dc["newGame"]["seed"]
                else:
                    s = seed
                self.initGame(self.gameId, self.sc, dc, s)
                self.gameId = self.getNextGameId()
            elif commandType == "terminate":
                idToTerminate = dc["gameId"]
                if idToTerminate in self.games:
                    self.safeTerminate(dc)
                    self.cleanUp()
            elif commandType == "close":
                self.closeServer()
            elif commandType == "changelog":
                send = Factory.createMessageEvent(dc["fromId"], loc(lang, "changelog"))
                send["gameId"] = 0
                self.sc.sendJSON(send)
                self.sc.receiveJSON()
            elif dc["gameId"] in self.games:
                self.games[dc["gameId"]]["toProcessQueue"].put(dc)
            else:
                print("can't find a game with id " + str(dc["gameId"]))

    def closeServer(self):
        for gameId in self.games:
            self.games[gameId]["process"].kill()
        for client in self.clientList:
            client.kill()
        sys.exit(0)

    def safeTerminate(self, dc):
        gameId = dc["gameId"]
        if dc["fromId"] != self.games[gameId]["admin"]:
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
                        {"numberSent": numberSent, "recList": recList, "origin": chatId},
                        "fromId": admin}
                    self.initGame(gameId, sc, dc, s)

    def initGame(self, gameId, sc, dc, seed):
        self.games[gameId] = {"toProcessQueue": SimpleQueue()}
        self.games[gameId]["admin"] = dc["fromId"]
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


def startTelegramClient(recQueue, sendQueue):
    tclient = TelegramClient(recQueue, sendQueue)
    tclient.run()


def startTesting(recQueue, sendQueue):
    testClient = SystemTestMain(recQueue, sendQueue)
    testClient.main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-S", "--systemtest", help="run the system tests", action="store_true")
    parser.add_argument("-T", "--telegram", help="enables the Telegram Client", action="store_true")
    args = parser.parse_args()
    main = Main(enableSysTestClient=args.systemtest, enableTclient=args.telegram)
    main.main()
