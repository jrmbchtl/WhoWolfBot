import json
import requests

from . import Factory
from .GameData import GameData
from .Player import Player
from .characters import Teams
from .characters.Character import Character
from .characters.Types import CharacterType
from .characters.village.Dorfbewohner import Dorfbewohner, Dorfbewohnerin
from .characters.village.Hexe import Hexe
from .characters.village.Jaeger import Jaeger
from .characters.village.Seherin import Seherin
from .characters.werwolf import wake
from .characters.werwolf.Terrorwolf import Terrorwolf
from .characters.werwolf.Werwolf import Werwolf
from .characters.werwolf.Wolfshund import Wolfshund


class Server(object):
    def __init__(self, seed, sc, admin, origin, gameQueue, gameId):
        super(Server, self)
        self.gameData = GameData(seed=seed, players={}, sc=sc, admin=admin, origin=origin,
                                 gameQueue=gameQueue, gameId=gameId, menuMessageId=None)
        self.accusedDict = {}

    def start(self):
        self.register()
        self.rollRoles()
        while not self.checkGameOver():
            self.night()
            if self.checkGameOver():
                break
            if len(self.accusedDict) <= 3:
                self.accuseAll()
            else:
                self.accuse()
            self.vote()

    def updateRegisterMenu(self, disable=False):
        message = ("Viel Spass beim Werwolf spielen!\n\nBitte einen privaten Chat mit dem Bot "
                   "starten, bevor das Spiel beginnt!\n\nUm das Spiel in seiner vollen Breite "
                   "genießen zu können, empfiehlt es sich bei sehr schmalen Bildschirmen, "
                   "diese quer zu verwenden.\n\n")
        message += 'Spieler:\n'
        for player in self.gameData.getPlayers():
            message += self.gameData.getPlayers()[player].getName() + "\n"
        if not disable:
            options = ["Mitspielen/Aussteigen", "Start", "Cancel"]
        else:
            options = []
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
        self.updateRegisterMenu()
        rec = self.gameData.getNextMessageDict()
        while (rec["commandType"] != "startGame"
               or rec["startGame"]["senderId"] != self.gameData.getAdmin()
               or len(self.gameData.getPlayers()) < 4):
            if rec["commandType"] == "register":
                if rec["register"]["id"] not in self.gameData.getPlayers():
                    self.gameData.sendJSON(
                        Factory.createMessageEvent(rec["register"]["id"], "Ich bin der Werwolfbot"))
                    tmp = self.gameData.getNextMessageDict()
                    if tmp["feedback"]["success"] == 0:
                        self.gameData.sendJSON(Factory.createMessageEvent(
                            self.gameData.getOrigin(),
                            "@" + rec["register"]["name"]
                            + ", bitte öffne einen privaten Chat mit mir"))
                        self.gameData.dumpNextMessageDict()
                        rec = self.gameData.getNextMessageDict()
                        continue
                    else:
                        self.gameData.sendJSON(
                            Factory.createMessageEvent(rec["register"]["id"],
                                                       "", tmp["feedback"]["messageId"],
                                                       Factory.EditMode.DELETE))
                        self.gameData.dumpNextMessageDict()
                        player = Player(rec["register"]["name"])
                        self.gameData.getPlayers()[rec["register"]["id"]] = player
                else:
                    self.gameData.getPlayers().pop(rec["register"]["id"], None)
                self.updateRegisterMenu()
            rec = self.gameData.getNextMessageDict()
        self.updateRegisterMenu(True)

    def rollRoles(self):
        playerList: list = self.gameData.getPlayerList()
        self.gameData.shuffle(playerList)

        werwolfRoleList = getWerwolfRoleList(len(playerList))
        dorfRoleList = getVillagerRoleList()

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
            self.gameData.dumpNextMessageDict()

    def night(self):
        self.gameData.sendJSON(Factory.createMessageEvent(
            self.gameData.getOrigin(), self.nightfall()))
        self.gameData.dumpNextMessageDict()

        sortedPlayerDict = self.gameData.getAlivePlayersSortedDict()
        wakeWerwolf = False
        for p in sortedPlayerDict:
            player = sortedPlayerDict[p]
            print("waking up " + player.getName())
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
            werwolfTarget: Character = self.gameData.getAlivePlayers()[werwolfTargetId]
            werwolfTarget.kill(self.gameData, werwolfTargetId)
        if self.gameData.getWitchTarget() is not None:
            witchTargetId = self.gameData.getWitchTarget()
            witchTarget: Character = self.gameData.getAlivePlayers()[witchTargetId]
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
            choice, option = self.anklageOptions()
            option = self.gameData.getAlivePlayers()[player].getName() + option
            options.append(option)
            idToChoice[player] = choice
        text = self.anklageIntro()
        self.gameData.sendJSON(Factory.createChoiceFieldEvent(
            self.gameData.getOrigin(), text, options))
        messageId = self.gameData.getNextMessageDict()["feedback"]["messageId"]

        newText = ""
        while len(self.accusedDict) < 3:
            rec = self.gameData.getNextMessageDict()
            self.accusedDict[rec["reply"]["fromId"]] = \
                self.gameData.getAlivePlayerList()[rec["reply"]["choiceIndex"]]
            newText = text + "\n\n"
            for entry in self.accusedDict:
                target = self.accusedDict[entry]
                newText += self.gameData.idToName(entry)
                newText += self.anklageText(idToChoice[target], self.gameData.idToName(target))
            self.gameData.sendJSON(Factory.createChoiceFieldEvent(
                self.gameData.getOrigin(), text, options, messageId, Factory.EditMode.EDIT))
            self.gameData.dumpNextMessageDict()

        self.gameData.sendJSON(Factory.createMessageEvent(
            self.gameData.getOrigin(), newText, messageId, Factory.EditMode.EDIT))
        self.gameData.dumpNextMessageDict()

    def anklageOptions(self):
        switcher = {
            0: " anklagen",
            1: " bezichtigen",
            2: " Verrat vorwerfen",
            3: " anprangern",
            4: " anschuldigen",
            5: " beschuldigen"
        }
        choice = self.gameData.randrange(0, 6)
        return choice, switcher[choice]

    def anklageIntro(self):
        switcher = {
            0: "Es ist Zeit, anzuklagen!",
            1: "Nach einer turbulenten Nacht geht es in Düsterwald heiß her.",
            2: "Nach einer solchen Nacht wird in Düsterwald blind beschuldigt.",
            3: ("Die Dorfbewohner wollen die Übeltäter im Dorf entlarven und beginnen "
                "mit den Beschuldigungen."),
            4: "Die Dorfbewohner versuchen durch wildes Beschuldigen, die Werwölfe zu enttarnen.",
            5: ("Jeder versucht, sein eigenes Leben zu schützen und schiebt deshalb die "
                "Schuld auf Andere."),
            6: "Die Dorfbewohner wollen jemanden für die Verbrechen der Nacht beschuldigen.",
            7: ("Eine Diskussion entbrandet, wer an den schrecklichen Taten der Nacht "
                "schuld sein könnte."),
            8: ("Eine heiße Diskussion beginnt in Düsterwald. Vage Gerüchte werden auf einmal zu "
                "harten Fakten, Werwölfe tarnen sich als normale Büger und harmlose Dorfbewohner "
                "werden des brutalen Mordes beschuldigt."),
            9: "Lasset die Beschuldigungsspiele beginnen!"
        }
        return switcher[self.gameData.randrange(0, 10)]

    def anklageText(self, option, name):
        switcher = {
            0: " möchte nun " + name + " anklagen.",
            1: " bezichtigt nun " + name + ".",
            2: " wirft nun " + name + " Verrat vor!",
            3: " will nun " + name + " anprangern!",
            4: " trifft nun Anschuldigungen gegen " + name + ".",
            5: " beschuldigt jetzt " + name + "."
        }
        return switcher[option]

    def vote(self):
        idToChoice, voteDict = self.getVoteDict()
        if GameData.uniqueDecision(voteDict):
            victimIndex = GameData.getDecision(voteDict)
            victimId = self.gameData.getAlivePlayerList()[victimIndex]
            dm = self.voteJudgement(idToChoice[victimId])
            self.gameData.getAlivePlayers()[victimId].kill(self.gameData, victimId, dm)
        else:
            text = self.pattRevote()
            idToChoice, voteDict = self.getVoteDict(text)
            if GameData.uniqueDecision(voteDict):
                victimIndex = GameData.getDecision(voteDict)
                victimId = self.gameData.getAlivePlayerList()[victimIndex]
                dm = self.voteJudgement(idToChoice[victimId])
                self.gameData.getAlivePlayers()[victimId].kill(self.gameData, victimId, dm)
            else:
                text = self.pattNoKill()
                self.gameData.sendJSON(Factory.createMessageEvent(self.gameData.getOrigin(), text))
                self.gameData.dumpNextMessageDict()

    def getVoteDict(self, text=None):
        voteDict = {}  # stores who voted for which index

        if text is None:
            text = self.voteIntro()
        options = []
        idToChoice = {}
        for player in self.gameData.getAlivePlayers():
            playerName = self.gameData.getAlivePlayers()[player].getName()
            choice, option = self.voteOptions()
            idToChoice[player] = choice
            option = playerName + option
            options.append(option)
        self.gameData.sendJSON(Factory.createChoiceFieldEvent(
            self.gameData.getOrigin(), text, options))
        messageId = self.gameData.getNextMessageDict()["feedback"]["messageId"]

        newText = ""
        while len(voteDict) < len(self.gameData.getAlivePlayers()):
            rec = self.gameData.getNextMessageDict()
            if rec["commandType"] == "reply":
                voteDict[rec["reply"]["fromId"]] = rec["reply"]["choiceIndex"]

                newText = text + "\n"
                for key in voteDict:
                    targetId = self.gameData.getAlivePlayerList()[voteDict[key]]
                    targetName = self.gameData.idToName(targetId)
                    voterName = self.gameData.idToName(key)
                    text += "\n" + voterName
                    text += self.votedFor(idToChoice[targetId], targetName)

                self.gameData.sendJSON(Factory.createChoiceFieldEvent(
                    self.gameData.getOrigin(), newText, options, messageId, Factory.EditMode.EDIT))
                self.gameData.dumpNextMessageDict()

        self.gameData.sendJSON(Factory.createMessageEvent(
            self.gameData.getOrigin(), newText, messageId, Factory.EditMode.EDIT))
        self.gameData.getNextMessageDict()
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
                self.gameData.getOrigin(), self.allDead()))
            self.gameData.dumpNextMessageDict()
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
                    Factory.createMessageEvent(self.gameData.getOrigin(), self.werwoelfeWin()))
            else:
                self.gameData.sendJSON(
                    Factory.createMessageEvent(self.gameData.getOrigin(), self.dorfWin()))
            self.gameData.dumpNextMessageDict()
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


def removeCharacterTypeFromList(ls, ct):
    i = 0
    while i < len(ls):
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
