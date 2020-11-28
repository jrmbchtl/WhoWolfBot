import json
import requests
import os

from . import Factory
from .GameData import GameData
from .Player import Player
from .characters import Teams
from .characters.Types import CharacterType
from .characters.village.BadassBastard import BadassBastard
from .characters.village.Berserk import Berserk
from .characters.village.Cupid import Cupid
from .characters.village.Psychopath import Psychopath
from .characters.village.Redhat import Redhat
from .characters.village.Villager import Villager, Villagerf
from .characters.village.Witch import Witch
from .characters.village.Hunter import Hunter
from .characters.village.Seer import Seer
from .characters.werewolf import wake
from .characters.werewolf.Terrorwolf import Terrorwolf
from .characters.werewolf.Werewolf import Werewolf
from .characters.werewolf.Whitewolf import Whitewolf
from .characters.werewolf.Wolfdog import Wolfdog
from src.main.localization import getLocalization as loc


class Server(object):
    def __init__(self, seed, sc, dc, gameQueue, gameId, deleteQueue):
        super(Server, self)

        self.gameData = GameData(seed=seed, players={}, sc=sc, dc=dc, gameQueue=gameQueue,
                                 gameId=gameId, menuMessageId=None, deleteQueue=deleteQueue)
        self.accusedDict = {}
        self.enabledRoles = ["wolfdog", "terrorwolf", "seer", "witch", "hunter"]
        self.disabledRoles = ["badassbastard", "redhat", "whitewolf", "cupid", "berserk", "psycho"]
        self.settingsMessageId = None

    def start(self):
        self.setLanguage()
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

    def setLanguage(self):
        message = loc(self.gameData.getLang(), "languageQuestion")
        dc = loc()
        options = []
        for lang in dc:
            options.append(lang)
        self.gameData.sendJSON(Factory.createChoiceFieldEvent(self.gameData.getAdmin(), message,
                                                              options))
        messageId = self.gameData.getNextMessage(
            commandType="feedback", fromId=self.gameData.getAdmin())["feedback"]["messageId"]
        choice = self.gameData.getNextMessage(commandType="reply", fromId=self.gameData.getAdmin())
        self.gameData.setLang(options[choice["reply"]["choiceIndex"]])
        self.gameData.sendJSON(Factory.createMessageEvent(self.gameData.getAdmin(), "",
                                                          messageId, mode=Factory.EditMode.DELETE))
        self.gameData.dumpNextMessage(commandType="feedback", fromId=self.gameData.getAdmin())

    def updateRegisterMenu(self, disable=False):
        message = loc(self.gameData.getLang(), "gameMenu")
        message += loc(self.gameData.getLang(), "players") + ":\n"
        for player in self.gameData.getPlayers():
            message += self.gameData.getPlayers()[player].getName() + "\n"
        if not disable:
            options = [loc(self.gameData.getLang(), "join"),
                       loc(self.gameData.getLang(), "start"),
                       loc(self.gameData.getLang(), "cancel")]
        else:
            options = [loc(self.gameData.getLang(), "cancel")]
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
                        Factory.createMessageEvent(rec["fromId"],
                                                   loc(self.gameData.getLang(), "hello")))
                    tmp = self.gameData.getNextMessage(commandType="feedback")
                    if tmp["feedback"]["success"] == 0:
                        self.gameData.sendJSON(Factory.createMessageEvent(
                            self.gameData.getOrigin(), rec["register"]["name"]
                            + loc(self.gameData.getLang(), "plsOpen")))
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
                role = revLookup(loc(self.gameData.getLang(), "roles"), rec["add"]["role"])
                if role not in self.enabledRoles and role in self.disabledRoles:
                    self.enabledRoles.append(role)
                    self.disabledRoles.remove(role)
                    self.sendSettings()
            elif rec["commandType"] == "remove":
                role = revLookup(loc(self.gameData.getLang(), "roles"), rec["remove"]["role"])
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
        text = loc(self.gameData.getLang(), "roleConfig")
        roles = self.enabledRoles.copy()
        for i in self.disabledRoles:
            roles.append(i)
        roles.sort()
        options = []
        for i in roles:
            role = loc(self.gameData.getLang(), "roles", i)
            if i in self.enabledRoles:
                pre = loc(self.gameData.getLang(), "removePre")
                post = loc(self.gameData.getLang(), "removePost")
                options.append(pre + role + post)
            if i in self.disabledRoles:
                pre = loc(self.gameData.getLang(), "addPre")
                post = loc(self.gameData.getLang(), "addPost")
                options.append(pre + role + post)
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

        werewolfRoleList = self.getWerewolfRoleList(len(playerList))
        villageRoleList = self.getVillagerRoleList()

        unique = [CharacterType.HUNTER, CharacterType.SEER, CharacterType.WITCH,
                  CharacterType.WOLFDOG, CharacterType.TERRORWOLF, CharacterType.BADDASSBASTARD,
                  CharacterType.REDHAT, CharacterType.CUPID, CharacterType.BERSERK,
                  CharacterType.PSYCHOPATH]

        group_mod = self.gameData.random() * 0.2 + 0.9
        werewolfAmount = int(round(len(playerList) * (1.0 / 3.5) * group_mod, 0))
        for i, p in enumerate(playerList):
            if i < werewolfAmount:
                role = werewolfRoleList[self.gameData.randrange(0, len(werewolfRoleList))]
                self.gameData.getPlayers()[p].setCharacter(role)
                if role.getCharacterType() in unique:
                    removeCharacterTypeFromList(werewolfRoleList, role.getCharacterType())
            else:
                role = villageRoleList[self.gameData.randrange(0, len(villageRoleList))]
                self.gameData.getPlayers()[p].setCharacter(role)
                if role.getCharacterType() in unique:
                    removeCharacterTypeFromList(villageRoleList, role.getCharacterType())
                if role.getCharacterType() == CharacterType.HUNTER:
                    if "redhat" in self.enabledRoles:
                        for i in range(0, 28):
                            villageRoleList.append(Redhat())
            self.gameData.sendJSON(
                Factory.createMessageEvent(
                    p, self.gameData.getPlayers()[p].getCharacter().getDescription(self.gameData)))
            self.gameData.dumpNextMessage(commandType="feedback")

    def night(self):
        self.gameData.sendJSON(Factory.createMessageEvent(
            self.gameData.getOrigin(), self.nightfall()))
        self.gameData.dumpNextMessage(commandType="feedback")

        sortedPlayerDict = self.gameData.getAlivePlayersSortedDict()
        wakeWerewolf = False
        for p in sortedPlayerDict:
            player = sortedPlayerDict[p]
            if player.getCharacter().getRole().value[0] < 0:
                player.getCharacter().wakeUp(self.gameData, p)
            elif not wakeWerewolf:
                wakeWerewolf = True
                wake.wake(self.gameData)
                player.getCharacter().wakeUp(self.gameData, p)
            else:
                player.getCharacter().wakeUp(self.gameData, p)

        tl = []
        for target in self.gameData.getNightlyTarget():
            tl.append(target)
            self.killTarget(target)
        for t in tl:
            self.gameData.removeNightlyTarget(t)

    def killTarget(self, targetId):
        if targetId in self.gameData.getAlivePlayers():
            target = self.gameData.getAlivePlayers()[targetId].getCharacter()
            target.kill(self.gameData, targetId)

    def accuseAll(self):
        self.accusedDict = {}
        for player in self.gameData.getAlivePlayers():
            self.accusedDict[player] = player

    def accuse(self):
        self.accusedDict = {}
        idToChoice = {}
        options = []
        for player in self.gameData.getAlivePlayers():
            name = self.gameData.getAlivePlayers()[player].getName()
            choice, option = self.accuseOptions(name)
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

    def accuseOptions(self, name):
        pre = loc(self.gameData.getLang(), "accuseOptionsPre")
        post = loc(self.gameData.getLang(), "accuseOptionsPost")
        choice = self.gameData.randrange(0, len(pre))
        return choice, pre[str(choice)] + name + post[str(choice)]

    def accuseIntro(self):
        dc = loc(self.gameData.getLang(), "accuseIntro")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def accuseText(self, option, name):
        pre = loc(self.gameData.getLang(), "accuseTextPre", option)
        post = loc(self.gameData.getLang(), "accuseTextPost", option)
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
            choice, option = self.voteOptions(playerName)
            idToChoice[player] = choice
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
        dc = loc(self.gameData.getLang(), "voteIntro")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def voteOptions(self, name):
        pre = loc(self.gameData.getLang(), "voteOptionsPre")
        post = loc(self.gameData.getLang(), "voteOptionsPost")
        choice = self.gameData.randrange(0, len(pre))
        return choice, pre[str(choice)] + name + post[str(choice)]

    def votedFor(self, option, name):
        pre = loc(self.gameData.getLang(), "votedForPre", option)
        post = loc(self.gameData.getLang(), "votedForPost", option)
        return pre + name + post

    def voteJudgement(self, option):
        return loc(self.gameData.getLang(), "voteJudgement", option)

    def pattRevote(self):
        dc = loc(self.gameData.getLang(), "pattRevote")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def pattNoKill(self):
        dc = loc(self.gameData.getLang(), "pattNoKill")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def nightfall(self):
        dc = loc(self.gameData.getLang(), "nightfall")
        return dc[str(self.gameData.randrange(0, len(dc)))]

    def checkGameOver(self):
        if len(self.gameData.getAlivePlayers()) == 0:
            self.gameData.sendJSON(Factory.createMessageEvent(
                self.gameData.getOrigin(), self.allDead(), highlight=True))
            self.gameData.dumpNextMessage(commandType="feedback")
            return True
        else:
            if len(self.gameData.getAlivePlayers()) == 2:
                ids = self.gameData.getAlivePlayerList()
                if self.gameData.getAlivePlayers()[ids[0]].getCharacter().getBeloved() == ids[1]:
                    self.gameData.sendJSON(
                        Factory.createMessageEvent(self.gameData.getOrigin(), self.loveWin(),
                                                   highlight=True))
                    self.gameData.dumpNextMessage()
                    return True
            firstPlayerId = self.gameData.getAlivePlayerList()[0]
            team = self.gameData.getAlivePlayers()[firstPlayerId].getCharacter().getTeam()
            for player in self.gameData.getAlivePlayers():
                if self.gameData.getAlivePlayers()[player].getCharacter().getTeam() == team:
                    continue
                else:
                    return False
            if team == Teams.TeamType.WEREWOLF:
                self.gameData.sendJSON(
                    Factory.createMessageEvent(self.gameData.getOrigin(), self.werewolfWin(),
                                               highlight=True))
            elif team == Teams.TeamType.WHITEWOLF:
                self.gameData.sendJSON(
                    Factory.createMessageEvent(self.gameData.getOrigin(), self.whitewolfWin(),
                                               highlight=True))
            else:
                self.gameData.sendJSON(
                    Factory.createMessageEvent(self.gameData.getOrigin(), self.villageWin(),
                                               highlight=True))
            self.gameData.dumpNextMessage(commandType="feedback")
            return True

    def allDead(self):
        dc = loc(self.gameData.getLang(), "allDeadPre")
        choice = self.gameData.randrange(0, len(dc))
        if choice == 8:
            pre = dc[str(choice)]
            post = loc(self.gameData.getLang(), "allDeadPost")
            msg = pre + str(json.loads(requests.get("http://api.open-notify.org/astros.json")
                                       .text)["number"]) + post
        else:
            msg = dc[str(choice)]
        return msg

    def werewolfWin(self):
        dc = loc(self.gameData.getLang(), "werewolfWin")
        choice = self.gameData.randrange(0, len(dc))
        return dc[str(choice)]

    def whitewolfWin(self):
        dc = loc(self.gameData.getLang(), "whitewolfWin")
        choice = self.gameData.randrange(0, len(dc))
        return dc[str(choice)]

    def villageWin(self):
        dc = loc(self.gameData.getLang(), "villageWin")
        choice = self.gameData.randrange(0, len(dc))
        return dc[str(choice)]

    def loveWin(self):
        dc = loc(self.gameData.getLang(), "loveWin")
        choice = self.gameData.randrange(0, len(dc))
        return dc[str(choice)]

    def getWerewolfRoleList(self, amountOfPlayers):
        werewolfRoleList = []
        for i in range(0, 40):
            werewolfRoleList.append(Werewolf())
        if amountOfPlayers >= 6 and "wolfdog" in self.enabledRoles:
            for i in range(0, 40):
                werewolfRoleList.append(Wolfdog())
        if amountOfPlayers >= 6 and "whitewolf" in self.enabledRoles:
            for i in range(0, 40):
                werewolfRoleList.append(Whitewolf())
        if "terrorwolf" in self.enabledRoles:
            for i in range(0, 40):
                werewolfRoleList.append(Terrorwolf())
        return werewolfRoleList

    def getVillagerRoleList(self):
        villageRoleList = []
        for i in range(0, 30):
            villageRoleList.append(Villager())
            villageRoleList.append(Villagerf())
        if "hunter" in self.enabledRoles:
            for i in range(0, 28):
                villageRoleList.append(Hunter())
        if "seer" in self.enabledRoles:
            for i in range(0, 28):
                villageRoleList.append(Seer())
        if "witch" in self.enabledRoles:
            for i in range(0, 28):
                villageRoleList.append(Witch())

        return self.getVillagerRoleListExtended(villageRoleList)

    def getVillagerRoleListExtended(self, villageRoleList):
        if "badassbastard" in self.enabledRoles:
            for i in range(0, 28):
                villageRoleList.append(BadassBastard())
        if "cupid" in self.enabledRoles:
            for i in range(0, 28):
                villageRoleList.append(Cupid())
        if "berserk" in self.enabledRoles:
            for i in range(0, 28):
                villageRoleList.append(Berserk())
        if "psycho" in self.enabledRoles:
            for i in range(0, 28):
                villageRoleList.append(Psychopath())
        return villageRoleList


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
