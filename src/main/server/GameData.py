import random


class GameData(object):
    """stores data for each game"""

    def __init__(self, seed, players, sc, admin, origin, gameQueue, gameId,
                 menuMessageId):
        super(GameData, self).__init__()
        random.seed(seed)
        self.players = players
        self.sc = sc
        self.admin = admin
        self.origin = origin
        self.gameQueue = gameQueue
        self.gameId = gameId
        self.menuMessageId = menuMessageId
        self.werwolfTarget = None
        self.witchTarget = None

    def getNextMessageDict(self):
        while self.gameQueue.empty():
            pass
        return self.gameQueue.get()

    def dumpNextMessageDict(self):
        while self.gameQueue.empty():
            pass
        print("Dumped: " + str(self.gameQueue.get()))

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
        for player in self.players:
            playerList.append(player)
        return playerList

    def getAlivePlayersSortedDict(self):
        sortedDict = []
        while len(sortedDict) < len(self.getAlivePlayers()):
            maximum = None
            for player in self.getAlivePlayers():
                if player in sortedDict:
                    continue
                playerValue = self.getAlivePlayers()[player].getCharacter().getRole().value
                if maximum is None:
                    maximum = playerValue
                elif maximum < playerValue:
                    maximum = playerValue
            for player in self.getAlivePlayers():
                if self.getAlivePlayers()[player].getCharacter().getRole() == maximum:
                    if player in sortedDict:
                        continue
                    sortedDict[player] = self.getAlivePlayers()[player]
                    break
        return sortedDict

    def sendJSON(self, dc):
        dc["gameId"] = self.gameId
        self.sc.sendJSON(dc)

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
