from ..Types import CharacterType
from ..Teams import VillagerTeam
import random
from ... import Factory
from ..Types import TeamType


class Seherin(VillagerTeam):
    def __init__(self, isAlive=True):
        super(Seherin, self).__init__(CharacterType.SEHERIN, isAlive)
        self.descriptions = {
            0: """Du bist die Seherin. Diese erwacht jede Nacht, sucht sich einen Bewohner \
            aus und erfährt, ob dieser zu den Werwölfen gehört oder nicht.""",
            1: """Du bist die Seherin. Die Seherin hat die Fähigkeit, jede Nacht über einen \
            Mitspieler zu erfahren, ob dieser zu den Werwölfen gehört.""",
            2: """Bei deinem Charakter handelt es sich um die Seherin. Jede Nacht erhält sie \
            Einsicht über einen Spieler, ob dieser zu den Werwölfen gehört.""",
            3: """Du bist die Seherin. Die Seherin erwählt jede Nacht einen Spieler. Sie erfährt, \
            ob dieser gut oder böse ist.""",
            4: """Du bist die Seherin. Die Seherin erwacht, während alle anderen schlafen und darf \
            sich eine Person aussuchen, über die sie erfahren will, ob diese gut oder böse ist. \
            Da die Seherin zu jeder Runde die Gruppenzugehörigkeit einer weiteren Person im Spiel \
            kennt, kann sie großen Einfluss nehmen, muss aber ihr Wissen vorsichtig einsetzen.""",
            5: """Dein Charakter ist die Seherin. Als diese erhälst du die Fähigkeit, \
            jede Nacht über eine ander Person zu erfahren, ob diese gut oder böse ist."""
        }

    def getDescription(self):
        return self.descriptions.get(random.randrange(0, 5))

    def wakeUp(self, gameData, playerId):
        options = []
        playerIndexList = []
        playerToOption = {}
        for player in gameData.getAlivePlayers():
            if player != playerId:
                option, text = seherinOptions(gameData.getAlivePlayers()[player].getName())
                options.append(text)
                playerToOption[player] = option
                playerIndexList = player
        text = seherinChooseTarget()
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        rec = gameData.getNextMessageDict()
        messageId = rec["feedback"]["messageId"]

        rec = gameData.getNextMessageDict()
        choice = rec["reply"]["choiceIndex"]

        gameData.sendJSON(
            Factory.createMessageEvent(playerId, text, messageId))
        gameData.dumpNextMessageDict()

        if gameData.getAlivePlayers()[playerIndexList[choice]].getTeam() == TeamType.WERWOLF:
            replyText = seherinWerwolf(choice, playerIndexList[choice].getName())
        else:
            replyText = seherinNoWerwolf(choice, playerIndexList[choice].getName())
        gameData.sendJSON(Factory.createMessageEvent(playerId, replyText))
        gameData.dumpNextMessageDict()


def seherinChooseTarget():
    desc_no = random.randrange(0, 10)
    if desc_no == 0:
        return "Die Seherin erwacht. Was wird sie tun?"
    elif desc_no == 1:
        return "Die Seherin schreckt aus dem Schlaf hoch. Über wen wird sie diese Nacht \
        ein Geheimnis herrausfinden?"
    elif desc_no == 2:
        return "Die Seherin erwacht aus einem Albtraum. Sie hat eine Runden 'Ich sehe was, was du \
        nicht siehst!' verloren. Das wird ihr jetzt nicht passieren!"
    elif desc_no == 3:
        return "Der Wecker der Seherin klingelt. Über wen will sie nun bespitzeln?"
    elif desc_no == 4:
        return "Die Seherin erwacht wie von einem Blitz getroffen. Wessen Geheimnis will sie diese \
        Nacht lüften?"
    elif desc_no == 5:
        return "Als die Seherin nachts aufwacht, verspürt sie starken Tatendrang - \
        was wird sie damit machen?"
    elif desc_no == 6:
        return "Die Seherin arbeitet nebenberuflich als Privatdetektiv. Was tut sie diese Nacht?"
    elif desc_no == 7:
        return "Die Seherin leidet unter Schlafstörungen. Was wird sie diese Nacht unternehmen?"
    elif desc_no == 8:
        return "Die Seherin ist leidenschaftliche Spannerin. Wen stalkt sie diese Nacht?"
    else:
        return "Die Seherin kann mal wieder nicht schlafen. Was tut sie diese Nacht?"


def seherinOptions(name):
    desc_no = random.randrange(0, 7)
    if desc_no == 0:
        return 0, name + " einsehen"
    elif desc_no == 1:
        return 1, name + " von der Gestapo überwachen lassen"
    elif desc_no == 2:
        return 2, "Informationen über " + name + " beim BND einholen"
    elif desc_no == 3:
        return 3, name + " bespitzeln"
    elif desc_no == 4:
        return 4, name + " beobachten"
    elif desc_no == 5:
        return 5, "Ein Auge auf " + name + " werfen"
    else:
        return 6, name + " ausspionieren"


def seherinWerwolf(option, name):
    if option == 0:
        return name + " gehört zu den Werwölfen."
    elif option == 1:
        return "Die Gestapo hat herausgefunden: " + name + " ist ein Werwolf."
    elif option == 2:
        return "Der BND steckt dir zu: " + name + " ist böse!"
    elif option == 2:
        return name + " ist böse."
    elif option == 4:
        return "Es stellt sich heraus: " + name + " gehört den Bösen an."
    elif option == 5:
        return "Du siehst es mit deinen eigenen Augen: " + name \
               + " verwandelt sich Nachts in einen Werwolf!"
    else:
        return "Deine Ermittlungen haben ergeben: " + name + " ist ein Werwolf."


def seherinNoWerwolf(option, name):
    if option == 0:
        return name + " gehört nicht zu den Werwölfen."
    elif option == 1:
        return "Die Gestapo hat herausgefunden: " + name + " ist kein Werwolf."
    elif option == 2:
        return "Der BND steckt dir zu: " + name + " ist gut!"
    elif option == 3:
        return name + " ist gut."
    elif option == 4:
        return "Es stellt sich heraus: " + name + " gehört den Guten an."
    elif option == 5:
        return "Du siehst es mit deinen eigenen Augen: " + name \
               + " verwandelt sich Nachts nicht in einen Werwolf!"
    else:
        return "Deine Ermittlungen haben ergeben: " + name + " ist kein Werwolf."
