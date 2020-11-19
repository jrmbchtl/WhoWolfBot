import json
import requests
import os

from . import Factory
from .GameData import GameData
from .Player import Player
from .characters import Teams
from .characters.Types import CharacterType
from .characters.village.Dorfbewohner import Dorfbewohner, Dorfbewohnerin
from .characters.village.Hexe import Hexe
from .characters.village.Jaeger import Jaeger
from .characters.village.Seherin import Seherin
from .characters.werwolf import wake
from .characters.werwolf.Terrorwolf import Terrorwolf
from .characters.werwolf.Werwolf import Werwolf
from .characters.werwolf.Wolfshund import Wolfshund
from src.main.localization import getLocalization as loc

lang = "DE"


class Server(object):
    def __init__(self, seed, sc, dc, gameQueue, gameId, deleteQueue):
        super(Server, self)

        self.gameData = GameData(seed=seed, players={}, sc=sc, dc=dc, gameQueue=gameQueue,
                                 gameId=gameId, menuMessageId=None, deleteQueue=deleteQueue)
        self.accusedDict = {}
        self.enabledRoles = ["wolfdog", "terrorwolf", "seer", "witch", "hunter"]
        self.disabledRoles = []
        self.settingsMessageId = None

    def start(self):
        self.register()
        self.rollRoles()
        while not self.checkGameOver():
            self.night()
            if self.checkGameOver():
                break
            if len(self.gameData.getAlivePlayers()) <= 3:
                self.accuseAll()
            else:
                self.accuse()
            self.vote()
        messageId = self.gameData.getMenuMessageId()
        target = self.gameData.getOrigin()
        self.gameData.sendJSON({"eventType": "message", "message": {"messageId": messageId},
                                "target": target, "mode": "delete"})
        print("game " + str(self.gameData.gameId) + " is over")
        file = "games/" + str(self.gameData.gameId) + ".game"
        if os.path.isfile(file):
            os.remove(file)

    def updateRegisterMenu(self, disable=False):
        message = loc(lang, "gameMenu")
        message += loc(lang, "players") + ":\n"
        for player in self.gameData.getPlayers():
            message += self.gameData.getPlayers()[player].getName() + "\n"
        if not disable:
            options = [loc(lang, "join"), loc(lang, "start"), loc(lang, "cancel")]
        else:
            options = [loc(lang, "cancel")]
        if self.gameData.getMenuMessageId() is None:
            sendDict = Factory.createChoiceFieldEvent(self.gameData.getOrigin(), message, options)
        else:
            sendDict = Factory.createChoiceFieldEvent(self.gameData.getOrigin(),
                                                      message, options,
                                                      self.gameData.getMenuMessageId(),
                                                      Factory.EditMode.EDIT)
        self.gameData.sendJSON(sendDict)

        rec = self.gameData.getNextMessage(commandType="feedback")
        self.gameData.setMenuMessageId(rec["feedback"]["messageId"])

    def register(self):
        self.updateRegisterMenu()
        self.sendSettings()
        rec = self.gameData.getNextMessage()
        while (rec["commandType"] != "startGame"
               or rec["fromId"] != self.gameData.getAdmin()
               or len(self.gameData.getPlayers()) < 4):
            if rec["commandType"] == "register":
                if rec["fromId"] not in self.gameData.getPlayers():
                    self.gameData.sendJSON(
                        Factory.createMessageEvent(rec["fromId"], loc(lang, "hello")))
                    tmp = self.gameData.getNextMessage(commandType="feedback")
                    if tmp["feedback"]["success"] == 0:
                        self.gameData.sendJSON(Factory.createMessageEvent(
                            self.gameData.getOrigin(), rec["register"]["name"]
                            + loc(lang, "plsOpen")))
                        self.gameData.dumpNextMessage(commandType="feedback")
                    else:
                        self.gameData.sendJSON(
                            Factory.createMessageEvent(rec["fromId"],
                                                       "", tmp["feedback"]["messageId"],
                                                       Factory.EditMode.DELETE))
                        self.gameData.dumpNextMessage(commandType="feedback")
                        player = Player(rec["register"]["name"])
                        self.gameData.getPlayers()[rec["fromId"]] = player
                else:
                    self.gameData.getPlayers().pop(rec["fromId"], None)
                self.updateRegisterMenu()
            elif rec["commandType"] == "add":
                role = revLookup(loc(lang, "roles"), rec["add"]["role"])
                if role not in self.enabledRoles and role in self.disabledRoles:
                    self.enabledRoles.append(role)
                    self.disabledRoles.remove(role)
                    self.sendSettings()
            elif rec["commandType"] == "remove":
                role = revLookup(loc(lang, "roles"), rec["add"]["role"])
                if role in self.enabledRoles and role not in self.disabledRoles:
                    self.enabledRoles.remove(role)
                    self.disabledRoles.append(role)
                    self.sendSettings()
            rec = self.gameData.getNextMessage()
        self.updateRegisterMenu(True)
        self.gameData.sendJSON(
            Factory.createMessageEvent(self.gameData.getAdmin(), messageId=self.settingsMessageId,
                                       mode=Factory.EditMode.DELETE))
        self.gameData.dumpNextMessage(commandType="feedback")

    def sendSettings(self):
        target = self.gameData.getAdmin()
        text = loc(lang, "roleConfig")
        roles = self.enabledRoles.copy()
        for i in self.disabledRoles:
            roles.append(i)
        roles.sort()
        options = []
        for i in roles:
            role = loc(lang, "roles", i)
            if i in self.enabledRoles:
                options.append(role + " " + loc(lang, "remove"))
            if i in self.disabledRoles:
                options.append(role + " " + loc(lang, "add"))
        if self.settingsMessageId is None:
            messageId = 0
            mode = Factory.EditMode.WRITE
        else:
            messageId = self.settingsMessageId
            mode = Factory.EditMode.EDIT

        self.gameData.sendJSON(
            Factory.createChoiceFieldEvent(target, text, options, messageId, mode))
        self.settingsMessageId = \
            self.gameData.getNextMessage(commandType="feedback")["feedback"]["messageId"]

    def rollRoles(self):
        playerList: list = self.gameData.getPlayerList()
        self.gameData.shuffle(playerList)

        werwolfRoleList = self.getWerwolfRoleList(len(playerList))
        dorfRoleList = self.getVillagerRoleList()

        unique = [CharacterType.JAEGER, CharacterType.SEHERIN, CharacterType.HEXE,
                  CharacterType.WOLFSHUND, CharacterType.TERRORWOLF]

        group_mod = self.gameData.random() * 0.2 + 0.9
        werwolf_amount = int(round(len(playerList) * (1.0 / 3.5) * group_mod, 0))
        for i, p in enumerate(playerList):
            if i < werwolf_amount:
                role = werwolfRoleList[self.gameData.randrange(0, len(werwolfRoleList))]
                self.gameData.getPlayers()[p].setCharacter(role)
                if role.getCharacterType() in unique:
                    removeCharacterTypeFromList(werwolfRoleList, role.getCharacterType())
            else:
                role = dorfRoleList[self.gameData.randrange(0, len(dorfRoleList))]
                self.gameData.getPlayers()[p].setCharacter(role)
                if role.getCharacterType() in unique:
                    removeCharacterTypeFromList(dorfRoleList, role.getCharacterType())
            self.gameData.sendJSON(
                Factory.createMessageEvent(
                    p, self.gameData.getPlayers()[p].getCharacter().getDescription(self.gameData)))
            self.gameData.dumpNextMessage(commandType="feedback")

    def night(self):
        self.gameData.sendJSON(Factory.createMessageEvent(
            self.gameData.getOrigin(), self.nightfall()))
        self.gameData.dumpNextMessage(commandType="feedback")

        sortedPlayerDict = self.gameData.getAlivePlayersSortedDict()
        wakeWerwolf = False
        for p in sortedPlayerDict:
            player = sortedPlayerDict[p]
            if player.getCharacter().getRole().value[0] < 0:
                player.getCharacter().wakeUp(self.gameData, p)
            elif not wakeWerwolf:
                wakeWerwolf = True
                wake.wake(self.gameData)
                player.getCharacter().wakeUp(self.gameData, p)
            else:
                player.getCharacter().wakeUp(self.gameData, p)

        if self.gameData.getWerwolfTarget() is not None:
            werwolfTargetId = self.gameData.getWerwolfTarget()
            werwolfTarget = self.gameData.getAlivePlayers()[werwolfTargetId].getCharacter()
            werwolfTarget.kill(self.gameData, werwolfTargetId)
        if self.gameData.getWitchTarget() is not None:
            witchTargetId = self.gameData.getWitchTarget()
            witchTarget = self.gameData.getAlivePlayers()[witchTargetId].getCharacter()
            witchTarget.kill(self.gameData, witchTargetId)

    def accuseAll(self):
        self.accusedDict = {}
        for player in self.gameData.getAlivePlayers():
            self.accusedDict[player] = player

    def accuse(self):
        self.accusedDict = {}
        idToChoice = {}
        options = []
        for player in self.gameData.getAlivePlayers():
            choice, option = self.accuseOptions()
            option = self.gameData.getAlivePlayers()[player].getName() + option
            options.append(option)
            idToChoice[player] = choice
        text = self.accuseIntro()
        self.gameData.sendJSON(Factory.createChoiceFieldEvent(
            self.gameData.getOrigin(), text, options))
        messageId = self.gameData.getNextMessage(commandType="feedback")["feedback"]["messageId"]

        newText = ""
        while len(self.accusedDict) < 3:
            rec = self.gameData.getNextMessage(commandType="reply")
            if rec["fromId"] not in self.gameData.getAlivePlayers():
                continue
            self.accusedDict[rec["fromId"]] = \
                self.gameData.getAlivePlayerList()[rec["reply"]["choiceIndex"]]
            newText = text + "\n\n"
            for entry in self.accusedDict:
                target = self.accusedDict[entry]
                newText += self.gameData.idToName(entry)
                newText += self.accuseText(idToChoice[target], self.gameData.idToName(target))
            self.gameData.sendJSON(Factory.createChoiceFieldEvent(
                self.gameData.getOrigin(), newText, options, messageId, Factory.EditMode.EDIT))
            self.gameData.dumpNextMessage(commandType="feedback")

        self.gameData.sendJSON(Factory.createMessageEvent(
            self.gameData.getOrigin(), newText, messageId, Factory.EditMode.EDIT))
        self.gameData.dumpNextMessage(commandType="feedback")

    def accuseOptions(self):
        dc = loc(lang, "accuseOptions")
        choice = self.gameData.randrange(0, len(dc))
        return choice, dc[str(choice)]

    def accuseIntro(self):
        dc = loc(lang, "accuseIntro")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def accuseText(self, option, name):
        pre = loc(lang, "accuseTextPre", option)
        post = loc(lang, "accuseTextPost", option)
        return pre + name + post

    def vote(self):
        idToChoice, voteDict = self.getVoteDict()
        if GameData.uniqueDecision(voteDict):
            victimId = GameData.getDecision(voteDict)
            dm = self.gameData.idToName(victimId) + self.voteJudgement(idToChoice[victimId])
            self.gameData.getAlivePlayers()[victimId].getCharacter()\
                .kill(self.gameData, victimId, dm)
        else:
            text = self.pattRevote()
            idToChoice, voteDict = self.getVoteDict(text)
            if GameData.uniqueDecision(voteDict):
                victimId = GameData.getDecision(voteDict)
                dm = self.gameData.idToName(victimId) + self.voteJudgement(idToChoice[victimId])
                self.gameData.getAlivePlayers()[victimId].getCharacter()\
                    .kill(self.gameData, victimId, dm)
            else:
                text = self.pattNoKill()
                self.gameData.sendJSON(Factory.createMessageEvent(self.gameData.getOrigin(), text))
                self.gameData.dumpNextMessage(commandType="feedback")

    def getVoteDict(self, text=None):
        voteDict = {}  # stores who voted for which index

        if text is None:
            text = self.voteIntro()
        options = []
        idToChoice = {}
        indexToId = {}
        for index, p in enumerate(self.accusedDict):
            player = self.accusedDict[p]
            playerName = self.gameData.getAlivePlayers()[player].getName()
            choice, option = self.voteOptions()
            idToChoice[player] = choice
            option = playerName + option
            options.append(option)
            indexToId[index] = player
        self.gameData.sendJSON(Factory.createChoiceFieldEvent(
            self.gameData.getOrigin(), text, options))
        messageId = self.gameData.getNextMessage(commandType="feedback")["feedback"]["messageId"]

        newText = ""
        while len(voteDict) < len(self.gameData.getAlivePlayers()):
            rec = self.gameData.getNextMessage(commandType="reply")
            if rec["commandType"] == "reply":
                if rec["fromId"] not in self.gameData.getAlivePlayers():
                    continue
                voteDict[rec["fromId"]] = rec["reply"]["choiceIndex"]
                newText = text + "\n"
                for key in voteDict:
                    targetId = indexToId[voteDict[key]]
                    targetName = self.gameData.idToName(targetId)
                    voterName = self.gameData.idToName(key)
                    newText += "\n" + voterName
                    newText += self.votedFor(idToChoice[targetId], targetName)

                self.gameData.sendJSON(Factory.createChoiceFieldEvent(
                    self.gameData.getOrigin(), newText, options, messageId, Factory.EditMode.EDIT))
                self.gameData.dumpNextMessage(commandType="feedback")

        self.gameData.sendJSON(Factory.createMessageEvent(
            self.gameData.getOrigin(), newText, messageId, Factory.EditMode.EDIT))
        self.gameData.getNextMessage(commandType="feedback")
        # change voteDict to store voterId -> votedId
        for p in voteDict:
            voteDict[p] = indexToId[voteDict[p]]
        return idToChoice, voteDict

    def voteIntro(self):
        dc = loc(lang, "voteIntro")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def voteOptions(self):
        dc = loc(lang, "voteOptions")
        choice = self.gameData.randrange(0, len(dc))
        return choice, dc[str(choice)]

    def votedFor(self, option, name):
        pre = loc(lang, "votedForPre", option)
        post = loc(lang, "votedForPost", option)
        return pre + name + post

    def voteJudgement(self, option):
        return loc(lang, "voteJudgement", option)

    def pattRevote(self):
        dc = loc(lang, "pattRevote")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def pattNoKill(self):
        dc = loc(lang, "pattNoKill")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def nightfall(self):
        dc = loc(lang, "nightfall")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def checkGameOver(self):
        if len(self.gameData.getAlivePlayers()) == 0:
            self.gameData.sendJSON(Factory.createMessageEvent(
                self.gameData.getOrigin(), self.allDead(), highlight=True))
            self.gameData.dumpNextMessage(commandType="feedback")
            return True
        else:
            firstPlayerId = self.gameData.getAlivePlayerList()[0]
            team = self.gameData.getAlivePlayers()[firstPlayerId].getCharacter().getTeam()
            for player in self.gameData.getAlivePlayers():
                if self.gameData.getAlivePlayers()[player].getCharacter().getTeam() == team:
                    continue
                else:
                    return False
            if team == Teams.TeamType.WERWOLF:
                self.gameData.sendJSON(
                    Factory.createMessageEvent(self.gameData.getOrigin(), self.werewolfWin(),
                                               highlight=True))
            else:
                self.gameData.sendJSON(
                    Factory.createMessageEvent(self.gameData.getOrigin(), self.villageWin(),
                                               highlight=True))
            self.gameData.dumpNextMessage(commandType="feedback")
            return True

    def allDead(self):
        dc = loc(lang, "allDeadPre")
        choice = self.gameData.randrange(0, len(dc))
        if choice == 8:
            pre = dc[str(choice)]
            post = loc(lang, "allDeadPost")
            msg = pre + str(json.loads(requests.get("http://api.open-notify.org/astros.json")
                                       .text)["number"]) + post
        else:
            msg = dc[str(choice)]
        return msg

    def werewolfWin(self):
        dc = loc(lang, "werewolfWin")
        choice = self.gameData.randrange(0, len(dc))
        return dc[str(choice)]

    def villageWin(self):
        dc = loc(lang, "villageWin")
        choice = self.gameData.randrange(0, len(dc))
        return dc[str(choice)]

    def getWerwolfRoleList(self, amountOfPlayers):
        werwolfRoleList = []
        if amountOfPlayers >= 3 and "wolfdog" in self.enabledRoles:
            for i in range(0, 20):
                werwolfRoleList.append(Werwolf())
            for i in range(0, 40):
                werwolfRoleList.append(Wolfshund())
        else:
            for i in range(0, 60):
                werwolfRoleList.append(Werwolf())
        if "terrorwolf" in self.enabledRoles:
            for i in range(0, 40):
                werwolfRoleList.append(Terrorwolf())
        return werwolfRoleList

    def getVillagerRoleList(self):
        dorfRoleList = []
        for i in range(0, 30):
            dorfRoleList.append(Dorfbewohner())
            dorfRoleList.append(Dorfbewohnerin())
        if "hunter" in self.enabledRoles:
            for i in range(0, 28):
                dorfRoleList.append(Jaeger())
        if "seer" in self.enabledRoles:
            for i in range(0, 28):
                dorfRoleList.append(Seherin())
        if "witch" in self.enabledRoles:
            for i in range(0, 28):
                dorfRoleList.append(Hexe())
        return dorfRoleList


def removeCharacterTypeFromList(ls, ct):
    i = 0
    while i < len(ls):
        if ls[i].getCharacterType() == ct:
            del ls[i]
        else:
            i += 1


def revLookup(dc, value):
    for key in dc:
        if dc[key] == value:
            return key
