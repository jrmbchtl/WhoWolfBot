import random

from . import Factory
from .GameData import GameData
from .Player import Player
from .characters.Types import CharacterType
from .characters.village.Dorfbewohner import Dorfbewohner, Dorfbewohnerin
from .characters.village.Hexe import Hexe
from .characters.village.Jaeger import Jaeger
from .characters.village.Seherin import Seherin
from .characters.werwolf.Terrorwolf import Terrorwolf
from .characters.werwolf.Werwolf import Werwolf
from .characters.werwolf.Wolfshund import Wolfshund


class Server(object):
    def __init__(self, sc, admin, origin, gameQueue, gameId):
        super(Server, self)
        self.gameData = GameData(gameOver=False, players={}, sc=sc, admin=admin,
                                 origin=origin, gameQueue=gameQueue, gameId=gameId,
                                 menuMessageId=None)

    def start(self):
        self.register()
        self.rollRoles()
        while not self.gameData.getGameOver():
            self.night()
            if self.gameData.getGameOver():
                break
            self.accuse()
            self.vote()

    def updateRegisterMenu(self):
        message = "Viel Spass beim Werwolf spielen!\n\nBitte einen privaten Chat mit dem Bot starten, \
                   bevor das Spiel beginnt!\n\nUm das Spiel in seiner vollen Breite genießen zu \
                   können , empfiehlt es sich bei sehr schmalen Bildschirmen, \
                   diese quer zu verwenden.\n\n"
        message += 'Spieler:\n'
        for player in self.gameData.getPlayers():
            message += player.getName() + "\n"
        options = ["Mitspielen/Aussteigen", "Start", "Cancel"]
        sendDict = {}
        if self.gameData.getMenuMessageId() is None:
            sendDict = Factory.createChoiceFieldEvent(self.gameData.getOrigin(), message, options)
        else:
            sendDict = Factory.createChoiceFieldEvent(self.gameData.getOrigin(),
                                                      message, options,
                                                      self.gameData.getMenuMessageId(),
                                                      Factory.EditMode.EDIT)
        self.gameData.sendJSON(sendDict)

        rec = self.gameData.getNextMessageDict()
        self.gameData.setMenuMessageId(rec["feedback"]["messageId"])

    def register(self):
        rec = self.gameData.getNextMessageDict()
        while (rec["commandType"] != "startGame"
               or rec["startGame"]["senderId"] != self.gameData.getAdmin()
               or self.gameData.getPlayers().len() < 4):
            if rec["commandType"] == "register":
                if rec["register"]["id"] not in self.gameData.getPlayers():
                    Factory.createMessageEvent(rec["register"]["id"], "Ich bin der Werwolfbot")
                    tmp = self.gameData.getNextMessageDict()
                    if tmp["feedback"]["success"] == 0:
                        self.gameData.sendJSON(Factory.createMessageEvent(
                            self.gameData.getOrigin(),
                            "@" + rec["register"]["name"]
                            + ", bitte öffne einen privaten Chat mit mir"))
                        self.gameData.dumpNextMessageDict()
                        continue
                    else:
                        player = Player(rec["register"]["name"])
                        self.gameData.getPlayers()[rec["register"]["id"]] = player
                else:
                    self.gameData.getPlayers().pop(rec["register"]["id"], None)
                self.updateRegisterMenu()
                rec = self.gameData.getNextMessageDict()

    def rollRoles(self):
        playerList = self.gameData.getPlayerList()
        random.shuffle(playerList)

        werwolfRoleList = getWerwolfRoleList(len(playerList))
        dorfRoleList = getVillagerRoleList()

        unique = [CharacterType.JAEGER, CharacterType.SEHERIN, CharacterType.HEXE,
                  CharacterType.WOLFSHUND, CharacterType.TERROWOLF]

        group_mod = random.random() * 0.2 + 0.9
        werwolf_amount = int(round(len(playerList) * (1.0 / 3.5) * group_mod, 0))
        for i, p in enumerate(playerList):
            if i < werwolf_amount:
                role = werwolfRoleList[random.randrange(0, len(werwolfRoleList))]
                self.gameData.getPlayers()[p].setCharacter(role)
                if role.getCharacterType() in unique:
                    removeCharacterTypeFromList(werwolfRoleList, role.getCharacterType())
            else:
                role = dorfRoleList[random.randrange(0, len(dorfRoleList))]
                self.gameData.getPlayers()[p].setCharacter(role)
                if role.getCharacterType() in unique:
                    removeCharacterTypeFromList(dorfRoleList, role.getCharacterType())
            self.gameData.sendJSON(
                Factory.createMessageEvent(p, self.gameData.getPlayers()[p].getDescription()))
            self.gameData.dumpNextMessageDict()

    def night(self):
        pass

    def accuse(self):
        pass

    def vote(self):
        pass


def removeCharacterTypeFromList(ls, ct):
    i = 0
    while i < ls.len():
        if ls[i].getCharacterType() == ct:
            del ls[i]
        else:
            i += 1


def getWerwolfRoleList(amountOfPlayers):
    werwolfRoleList = []
    if amountOfPlayers >= 6:
        for i in range(0, 20):
            werwolfRoleList.append(Werwolf())
        for i in range(0, 40):
            werwolfRoleList.append(Wolfshund())
    else:
        for i in range(0, 60):
            werwolfRoleList.append(Werwolf())
    for i in range(0, 40):
        werwolfRoleList.append(Terrorwolf())
    return werwolfRoleList


def getVillagerRoleList():
    dorfRoleList = []
    for i in range(0, 30):
        dorfRoleList.append(Dorfbewohner())
        dorfRoleList.append(Dorfbewohnerin())
    for i in range(0, 28):
        dorfRoleList.append(Jaeger())
    for i in range(0, 28):
        dorfRoleList.append(Seherin())
    for i in range(0, 28):
        dorfRoleList.append(Hexe())
    return dorfRoleList
