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
        self.admin = dc["fromId"]
        self.origin = dc["newGame"]["origin"]
        self.players = players
        self.sc = sc
        self.gameQueue = gameQueue
        self.gameId = gameId
        self.menuMessageId = menuMessageId
        self.deleteQueue = deleteQueue
        self.lang = "EN"
        self.werewolfTarget = None
        self.whitewolfTarget = None
        self.witchTarget = None
        self.berserkTarget = []
        self.recList = []
        self.numberSent = 0
        if "numberSent" in dc["newGame"] and "recList" in dc["newGame"]:
            self.recList = dc["newGame"]["recList"]
            self.numberSent = dc["newGame"]["numberSent"]

    def getNextMessage(self, commandType=None, fromId=None):
        data = None
        index = 0
        writeBack = []
        while data is None:
            if index < len(self.recList):
                if (commandType is None or commandType == self.recList[index]["commandType"]) \
                        and (fromId is None or fromId == self.recList[index]["fromId"]):
                    data = self.recList.pop(index)
                else:
                    index += 1
            else:
                tmp = self.gameQueue.get()
                if (commandType is None or commandType == tmp["commandType"]) \
                        and (fromId is None or fromId == tmp["fromId"]):
                    data = tmp
                    self.appendToRecList(data)
                else:
                    writeBack.append(tmp)
        self.addToDeleteQueue(data)
        for i in writeBack:
            self.gameQueue.put(i)
        return data

    def dumpNextMessage(self, commandType=None, fromId=None):
        print("Dumped: " + str(self.getNextMessage(commandType, fromId)))

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
                    and i["target"] == data["fromId"]:
                inList = True
            self.deleteQueue.put(i)
        if not inList:
            self.deleteQueue.put({"target": data["fromId"],
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
            dc["lang"] = self.lang
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

    def setWerewolfTarget(self, werewolfTargetId):
        if werewolfTargetId is None:
            self.werewolfTarget = None
            return
        werewolfTarget = self.getAlivePlayers()[werewolfTargetId].getCharacter()
        print(self.getAlivePlayers()[werewolfTargetId].getName())
        if werewolfTarget.hasSecondLive():  # badass bastard
            werewolfTarget.removeSecondLive()
        elif not werewolfTarget.canBeKilled(self):  # redhat
            pass
        elif werewolfTarget.werewolfKillAttempt():  # berserk
            self.werewolfTarget = werewolfTargetId

    def getWerewolfTarget(self):
        return self.werewolfTarget

    def setWhitewolfTarget(self, whitewolfTarget):
        self.whitewolfTarget = whitewolfTarget

    def getWhitewolfTarget(self):
        return self.whitewolfTarget

    def setWitchTarget(self, witchTarget):
        self.witchTarget = witchTarget

    def getWitchTarget(self):
        return self.witchTarget

    def addBerserkTarget(self, target):
        self.berserkTarget.append(target)

    def setBerserkTarget(self, berserkTarget):
        if berserkTarget is None:
            self.berserkTarget = []
        else:
            self.berserkTarget = berserkTarget

    def getBerserkTarget(self):
        return self.berserkTarget

    def setLang(self, lang):
        self.lang = lang

    def getLang(self):
        return self.lang

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
