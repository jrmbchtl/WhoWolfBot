import os
import random
import json


class GameData(object):
    """stores data for each game"""

    def __init__(self, seed, players, sc, dc, gameQueue, gameId,
                 menuMessageId, deleteQueue):
        super(GameData, self).__init__()

        random.seed(seed)
        self.seed = seed
        self.admin = dc["newGame"]["senderId"]
        self.origin = dc["origin"]
        self.players = players
        self.sc = sc
        self.gameQueue = gameQueue
        self.gameId = gameId
        self.menuMessageId = menuMessageId
        self.deleteQueue = deleteQueue
        self.werwolfTarget = None
        self.witchTarget = None
        self.recList = []
        self.numberSent = 0
        if "numberSent" in dc["newGame"] and "recList" in dc["newGame"]:
            self.recList = dc["newGame"]["recList"]
            self.numberSent = dc["newGame"]["numberSent"]

    def getNextMessageDict(self):
        if len(self.recList) > 0:
            data = self.recList.pop(0)
            self.addToDeleteQueue(data)
            return data
        else:
            while self.gameQueue.empty():
                pass
            data = self.gameQueue.get()
            self.appendToRecList(data)
            self.addToDeleteQueue(data)
            return data

    def dumpNextMessageDict(self):
        if len(self.recList) > 0:
            data = self.recList.pop(0)
            self.addToDeleteQueue(data)
            print("Dumped: " + str(data))
        else:
            while self.gameQueue.empty():
                pass
            data = self.gameQueue.get()
            self.appendToRecList(data)
            self.addToDeleteQueue(data)
            print("Dumped: " + str(data))

    def addToDeleteQueue(self, data):
        if data["commandType"] != "feedback" or data["feedback"]["success"] == 0:
            return
        tmp = []
        while not self.deleteQueue.empty():
            item = self.deleteQueue.get()
            tmp.append(item)
        inList = False
        for i in tmp:
            if i["messageId"] == data["feedback"]["messageId"] \
                    and i["target"] == data["feedback"]["fromId"]:
                inList = True
            self.deleteQueue.put(i)
        if not inList:
            self.deleteQueue.put({"target": data["feedback"]["fromId"],
                                  "messageId": data["feedback"]["messageId"]})

    def appendToRecList(self, item):
        self.checkOrCreate()
        f = "games/" + str(self.gameId) + ".game"
        with open(f, "r") as jsonFile:
            data = json.load(jsonFile)
        data["recList"].append(item)
        with open(f, "w") as jsonFile:
            json.dump(data, jsonFile)

    def checkOrCreate(self):
        f = "games/" + str(self.gameId) + ".game"
        if not os.path.isfile(f):
            dc = {"seed": self.seed, "recList": [], "numberSent": 0, "admin": self.admin,
                  "chatId": self.origin}
            with open(f, "w") as jsonFile:
                json.dump(dc, jsonFile)

    def setPlayers(self, players):
        self.players = players

    def getPlayers(self):
        return self.players

    def getPlayerList(self):
        ls = []
        for player in self.players:
            ls.append(player)
        return ls

    def getAlivePlayers(self):
        alivePlayers = {}
        for player in self.players:
            if self.players[player].getCharacter().isAlive():
                alivePlayers[player] = self.players[player]
        return alivePlayers

    def getAlivePlayerList(self):
        playerList = []
        for player in self.getAlivePlayers():
            playerList.append(player)
        return playerList

    def getAlivePlayersSortedDict(self):
        sortedDict = {}
        while len(sortedDict) < len(self.getAlivePlayers()):
            minimum = None
            for player in self.getAlivePlayers():
                if player in sortedDict:
                    continue
                playerValue = self.getAlivePlayers()[player].getCharacter().getRole().value[0]
                if minimum is None:
                    minimum = playerValue
                elif minimum > playerValue:
                    minimum = playerValue
            for player in self.getAlivePlayers():
                if self.getAlivePlayers()[player].getCharacter().getRole().value[0] == minimum:
                    if player in sortedDict:
                        continue
                    sortedDict[player] = self.getAlivePlayers()[player]
                    break
        return sortedDict

    def sendJSON(self, dc):
        if self.numberSent > 0:
            self.numberSent -= 1
        else:
            dc["gameId"] = self.gameId
            self.sc.sendJSON(dc)
            self.incNumberSent()

    def incNumberSent(self):
        self.checkOrCreate()
        f = "games/" + str(self.gameId) + ".game"
        with open(f, "r") as jsonFile:
            data = json.load(jsonFile)
        data["numberSent"] += 1
        with open(f, "w") as jsonFile:
            json.dump(data, jsonFile)

    def setAdmin(self, admin):
        self.admin = admin

    def getAdmin(self):
        return self.admin

    def setOrigin(self, origin):
        self.origin = origin

    def getOrigin(self):
        return self.origin

    def setGameQueue(self, gameQueue):
        self.gameQueue = gameQueue

    def getGameQueue(self):
        return self.gameQueue

    def setMenuMessageId(self, menuMessageId):
        self.menuMessageId = menuMessageId

    def getMenuMessageId(self):
        return self.menuMessageId

    def setWerwolfTarget(self, werwolfTarget):
        self.werwolfTarget = werwolfTarget

    def getWerwolfTarget(self):
        return self.werwolfTarget

    def setWitchTarget(self, witchTarget):
        self.witchTarget = witchTarget

    def getWitchTarget(self):
        return self.witchTarget

    def randrange(self, start, stop, step=1):
        return random.randrange(start, stop, step)

    def random(self):
        return random.random()

    def shuffle(self, ls):
        random.shuffle(ls)

    def idToName(self, playerId):
        return self.players[playerId].getName()

    @staticmethod
    def getDecision(dc):
        choiceToAmount = {}
        for key in dc:
            if dc[key] not in choiceToAmount:
                choiceToAmount[dc[key]] = 1
            else:
                choiceToAmount[dc[key]] += 1

        maximum = 0
        unique = True
        for key in choiceToAmount:
            if choiceToAmount[key] > maximum:
                maximum = choiceToAmount[key]
                unique = True
            elif choiceToAmount[key] == maximum:
                unique = False

        if not unique:
            return None

        for key in choiceToAmount:
            if choiceToAmount[key] == maximum:
                return key

    @staticmethod
    def uniqueDecision(dc):
        if GameData.getDecision(dc) is None:
            return False
        else:
            return True
