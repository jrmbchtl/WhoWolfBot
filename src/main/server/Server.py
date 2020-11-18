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
        switcher = {
            0: "Es ist Zeit, jemanden hinzurichten!",
            1: "Die Dorfbewohner wollen die Verantwortlichen für die Morde sterben sehen!",
            2: "Die Abstimmung für die Hinrichtung beginnt.",
            3: "Wen wollt ihr hinrichten?",
            4: "Wer soll für die grausamen Verbrechen mit einem noch grausameren Tod bezahlen?",
            5: "Wer ist schuldig und muss sterben?",
            6: ("Auge um Auge, Zahn um Zahn - und wer muss aufgrund vager Gerüchte einen "
                "grauenvollen Tod sterben?"),
            7: "Die Demokratie wird entscheiden, wer hingerichtet wird!",
            8: "Das Dorf entscheidet, wer gelyncht wird!",
            9: "Lasset die Hinrichtungsspiele beginnen!"
        }
        return switcher[self.gameData.randrange(0, 10)]

    def voteOptions(self):
        switcher = {
            0: " hängen",
            1: " auf dem Scheiterhaufen verbrennen",
            2: " einen Schwedentrunk verabreichen",
            3: " vierteilen",
            4: " für das Gemeinwohl opfern",
            5: " ertränken",
            6: " von einem Felsen stürzen",
            7: " guillotinieren",
            8: " lebendig begraben",
            9: " steinigen"
        }
        choice = self.gameData.randrange(0, 10)
        return choice, switcher[choice]

    def votedFor(self, option, name):
        switcher = {
            0: " möchte " + name + " hängen!",
            1: " will " + name + " auf dem Scheiterhaufen sehen!",
            2: " möchte " + name + " den Schwedentrunk verabreichen.",
            3: " will " + name + " vierteilen.",
            4: " würde gerne " + name + " für das Gemeinwohl opfern.",
            5: " möchte " + name + " ertränken.",
            6: " will " + name + " von einem Felsen stürzen.",
            7: " will " + name + " unter die Guillotine legen.",
            8: " würde gerne " + name + " lebendig begraben.",
            9: " will " + name + " steinigen."
        }
        return switcher[option]

    def voteJudgement(self, option):
        switcher = {
            0: " wurde gehängt.",
            1: " wird auf dem Scheiterhaufen verbrannt!",
            2: " bekommt den Schwedentrunk verabreicht.",
            3: " wurde gevierteilt.",
            4: " hat sich für das Gemeinwohl opfern lassen.",
            5: " wurde ertränkt!",
            6: " wird von einem Felsen gestürzt.",
            7: " ist unter der Guillotine gelandet!",
            8: " wurde lebendig begraben.",
            9: " hat die Steinigung nicht überlebt."
        }
        return switcher[option]

    def pattRevote(self):
        switcher = {
            0: "Pattsituation - bitte nochmals abstimmen!",
            1: ("Das Dorf konnte sich nicht entscheiden, wer hingerichtet werden sollte. Deshalb "
                "muss die Abstimmung wiederholt werden."),
            2: "Die Abstimmung geht unentschieden aus und muss wiederholt werden.",
            3: ("Die Dorfgemeinschaft kann sich für keinen Schuldigen entscheiden und setzt daher "
                "Neuwahlen an."),
            4: ("Zustände wie in der Türkei: Es wird sooft gewählt, bis den Oberen das Ergebnis "
                "gefällt. Es wurden Neuwahlen angesetzt!"),
            5: ("Es kann nur eine Person hingerichtet werden, irgendjemand sollte seine Meinung "
                "ändern!"),
            6: "Hier kommt die Demokratie an ihre Grenzen: Die Wahl muss wiederholt werden.",
            7: ("Eine Koalition ist bei der Hinrichtung nicht möglich. Bitte entscheidet euch für "
                "einen Schuldigen."),
            8: ("Auf dem elekrtischen Stuhl ist nur Platz für eine Person. Bitte nochmals "
                "abstimmen!"),
            9: ("Wenn ihr zwei halbe Menschen hinrichtet, habt ihr mathematisch auch nur eine "
                "Person hingerichtet. Das Problem ist, dass dann beide tot sind. Entscheidet euch!")
        }
        return switcher[self.gameData.randrange(0, 10)]

    def pattNoKill(self):
        switcher = {
            0: ("Da sich das Dorf nicht auf einen Schuldigen einigen kann, wird heute niemand "
                "gelyncht."),
            1: "Die Demokratie ist überfordert und beschließt, niemanden hinzurichten.",
            2: "Nach einer intensiven aber ergebnislosen Diskussion kehren alle nach hause zurück.",
            3: "Mal wieder viel heiße Luft um Nichts - viel Anschuldigungen aber kein Ergebnis.",
            4: ("Bei dem versuch, alle Angeklagten zu hängen, reißt das Seil und das Dorf "
                "beschließt, heute niemanden hinzurichten."),
            5: ("Da die Diskussion zu hitzig wird, ohne ein Ergebnis zu zeigen, löst die Polizei "
                "die Versammlung auf und schickt alle Beteiligten fort."),
            6: ("Am Ende des Tages sind alle genervt, da letztlich keiner seine Meinung "
                "durchsetzen konnte."),
            7: ("Dieser Tag geht ohne einen Toten vorbei. Dies sorgt für Unmut unter den "
                "Dorfbewohnern, da die Werwölfe auch nächste Nacht nicht ruhen werden."),
            8: ("Die Dorfbewohner nehmen sich vor: Beim nächsten Mal erzielen wir bei der "
                "Abstimmung ein klares Ergebnis, doch momentan will keiner seine Meinung ändern. "
                "Vielleicht kann die kommende Nacht gegen ein Patt helfen?"),
            9: ("Da sich das Dorf nicht einigen konnte, beschließt es, eine Nacht über die "
                "Meinungen zu schlafen. Vielleicht wird man sich ja morgen einig.")
        }
        return switcher[self.gameData.randrange(0, 10)]

    def nightfall(self):
        switcher = {
            0: "Es wird Nacht in Düsterwald.",
            1: "Die Sonne geht langsam unter, es ist Zeit für alle, schlafen zu gehen.",
            2: ("Düsterwald bereitet sich auf eine turbulente Nacht vor und legt sich "
                "schlafen. Manche Individuen stellen sich jedoch einen Wecker..."),
            3: ("Die Nacht ist nicht weniger gefährlich als der Tag und die Dorfbewohner "
                "stellen sich darauf ein, sich vielleicht ein letztes Mal schlafen zu legen..."),
            4: "Sowie es langsam dunkel wird in Düsterwald, legen sich alle schlafen.",
            5: ("Nach einem anstrengenden Tag hoffen viele Dorfbewohner nun auf eine erholsame "
                "Nacht. Doch diese Nacht werden nicht alle gut schlafen..."),
            6: ("Die Straßen werden leer, in der Kneipe wurde schon vor einer halben Stunde "
                "das letzte Bier ausgeschenkt und Düsterwald legt sich schlafen."),
            7: ("Düsterwald legt sich schlafen - in der Hoffnung, in der Morgendämmerung "
                "wieder zu erwachen."),
            8: ("So manch Dorfbewohner hofft nun auf eine ruhige Nacht - andere schlecken sich "
                "schon das Maul..."),
            9: ("Die Dorfbewohner stoßen auf einen erfolgreichen Tag an und wünschen sich eine "
                "gute Nacht.")
        }
        return switcher[self.gameData.randrange(0, 10)]

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
                    Factory.createMessageEvent(self.gameData.getOrigin(), self.werwoelfeWin(),
                                               highlight=True))
            else:
                self.gameData.sendJSON(
                    Factory.createMessageEvent(self.gameData.getOrigin(), self.dorfWin(),
                                               highlight=True))
            self.gameData.dumpNextMessage(commandType="feedback")
            return True

    def allDead(self):
        switcher = {
            0: "Es sind alle tot.",
            1: "Das Dorf ist so lebendig wie Tschernobyl.",
            2: "In Düsterwald könnte jetzt ein Vulkan ausbrechen und niemand würde sterben.",
            3: "Düsterwald hat seine Letzte Ruhe gefunden.",
            4: "Jetzt leben nur noch Tiere in Düsterwald.",
            5: "Die Natur wird sich das kleine Örtchen ab jetzt Stück für Stück zurückholen.",
            6: "Die Zivilisation in Düsterwald ist ausgelöscht.",
            7: "Das Werwolfproblem ist beseitigt. Das Menschenproblem aber auch.",
            8: "Düsterwald hat jetzt "
               + str(json.loads(requests.get("http://api.open-notify.org/astros.json").text)
                     ["number"]) + " Einwohner weniger als das Weltall.",
            9: "Das Kapitel 'Düsterwald' ist jetzt endgültig abgeschlossen."
        }
        return switcher[self.gameData.randrange(0, 10)]

    def werwoelfeWin(self):
        switcher = {
            0: "Die Werwölfe gewinnen.",
            1: "Es war ein langer Kampf, aber die Werwölfe haben sich durchgesetzt.",
            2: "Es leben nur noch Werwölfe in Düsterwald!",
            3: "Es gibt keine Dorfbewohner mehr, die von den Werwölfen verspeißt werden können.",
            4: "Es wird wieder friedlich in Düsterwald, da hier jetzt nur noch Werwölfe leben.",
            5: "Die Werwölfe haben gesiegt.",
            6: "Die Werwölfe haben ihre Dominanz bewiesen.",
            7: "Die Werwölfe sind in Düsterwald anscheinend die stärkere Rasse.",
            8: "Mit dem Tod des letzten Dorfbewohners haben die Werwölfe jetzt ihre Ruhe.",
            9: ("Die Werwölfe veranstalten zur Feier des Tages einen Fest und verspeißen "
                "genussvoll den letzten Dorfbewohner.")
        }
        return switcher[self.gameData.randrange(0, 10)]

    def dorfWin(self):
        switcher = {
            0: "Das Dorf gewinnt.",
            1: "Es war ein langer Kampf, aber die Dorfbewohner haben sich durchgesetzt.",
            2: "Es leben keine Werwölfe mehr in Düsterwald!",
            3: "Es gibt keine Werwölfe mehr, die Dorfbewohner verspeißen wollen.",
            4: "Es wird wieder friedlich in Düsterwald, da hier nur noch Dorfbewohner leben.",
            5: "Die Dorfbewohner haben gesiegt.",
            6: "Die Dorfbewohner haben ihre Dominanz bewiesen.",
            7: "Die Werwölfe sind in Düsterwald anscheinend die unterlegene Rasse.",
            8: "Mit dem Tod des letzten Werwolfes haben die Dorfbewohner jetzt ihre Ruhe.",
            9: ("Die Dorfbewohner veranstalten zur Feier des Tages einen Fest und stopfen den "
                "letzten Werwolf aus.")
        }
        return switcher[self.gameData.randrange(0, 10)]

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


""""def makeReadable(text):
    exchange = {"ae": "ä", "oe": "ö", "ue": "ü", "Ae": "Ä", "Oe": "Ö", "Ue": "Ü"}
    tl = list(text)
    tl[0] = tl[0].capitalize()
    for index, i in enumerate(tl):
        if i == " " and index < len(tl):
            tl[index + 1] = tl[index + 1].capitalize()
    text = "".join(tl)
    for i in exchange:
        while i in text:
            text = text.replace(i, exchange[i])
    return text


def makeUnreadable(text):
    exchange = {"ae": "ä", "oe": "ö", "ue": "ü", "Ae": "Ä", "Oe": "Ö", "Ue": "Ü"}
    tl = list(text)
    tl[0] = tl[0].lower()
    for index, i in enumerate(tl):
        if i == " " and index < len(tl):
            tl[index + 1] = tl[index + 1].lower()
    text = "".join(tl)
    for i in exchange:
        while exchange[i] in text:
            text = text.replace(exchange[i], i)
    return text"""


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
