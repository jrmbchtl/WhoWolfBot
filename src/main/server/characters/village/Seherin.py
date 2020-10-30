from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.server.characters.Types import TeamType


class Seherin(VillagerTeam):
    def __init__(self, alive=True):
        super(Seherin, self).__init__(CharacterType.SEHERIN, alive)
        self.descriptions = {
            0: ("Du bist die Seherin. Diese erwacht jede Nacht, sucht sich einen Bewohner "
                "aus und erfährt, ob dieser zu den Werwölfen gehört oder nicht."),
            1: ("Du bist die Seherin. Die Seherin hat die Fähigkeit, jede Nacht über einen "
                "Mitspieler zu erfahren, ob dieser zu den Werwölfen gehört."),
            2: ("Bei deinem Charakter handelt es sich um die Seherin. Jede Nacht erhält sie "
                "Einsicht über einen Spieler, ob dieser zu den Werwölfen gehört."),
            3: ("Du bist die Seherin. Die Seherin erwählt jede Nacht einen Spieler. Sie erfährt, "
                "ob dieser gut oder böse ist."),
            4: ("Du bist die Seherin. Die Seherin erwacht, während alle anderen schlafen und darf "
                "sich eine Person aussuchen, über die sie erfahren will, ob diese gut oder böse "
                "ist. Da die Seherin zu jeder Runde die Gruppenzugehörigkeit einer weiteren Person "
                "im Spiel kennt, kann sie großen Einfluss nehmen, muss aber ihr Wissen vorsichtig "
                "einsetzen."),
            5: ("Dein Charakter ist die Seherin. Als diese erhälst du die Fähigkeit, "
                "jede Nacht über eine ander Person zu erfahren, ob diese gut oder böse ist.")
        }

    def getDescription(self, gameData):
        return self.descriptions.get(gameData.randrange(0, 6))

    def wakeUp(self, gameData, playerId):
        options = []
        playerIndexList = []
        playerToOption = {}
        for player in gameData.getAlivePlayers():
            if player != playerId:
                option, text = \
                    seherinOptions(gameData.getAlivePlayers()[player].getName(), gameData)
                options.append(text)
                playerToOption[player] = option
                playerIndexList.append(player)
        text = seherinChooseTarget(gameData)
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessageDict()["feedback"]["messageId"]

        choice = gameData.getNextMessageDict()["reply"]["choiceIndex"]

        gameData.sendJSON(
            Factory.createMessageEvent(playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessageDict()

        if gameData.getAlivePlayers()[playerIndexList[choice]].\
                getCharacter().getTeam() == TeamType.WERWOLF:
            replyText = seherinWerwolf(choice, gameData.getAlivePlayers()[playerIndexList[choice]]
                                       .getName())
        else:
            replyText = seherinNoWerwolf(choice, gameData.getAlivePlayers()[playerIndexList[choice]]
                                         .getName())
        gameData.sendJSON(Factory.createMessageEvent(playerId, replyText))
        gameData.dumpNextMessageDict()


def seherinChooseTarget(gameData):
    switcher = {
        0: "Die Seherin erwacht. Was wird sie tun?",
        1: ("Die Seherin schreckt aus dem Schlaf hoch. Über wen wird sie diese Nacht "
            "ein Geheimnis herrausfinden?"),
        2: ("Die Seherin erwacht aus einem Albtraum. Sie hat eine Runden 'Ich sehe was, was du "
            "nicht siehst!' verloren. Das wird ihr jetzt nicht passieren!"),
        3: "Der Wecker der Seherin klingelt. Über wen will sie nun bespitzeln?",
        4: ("Die Seherin erwacht wie von einem Blitz getroffen. Wessen Geheimnis will sie diese "
            "Nacht lüften?"),
        5: ("Als die Seherin nachts aufwacht, verspürt sie starken Tatendrang - "
            "was wird sie damit machen?"),
        6: "Die Seherin arbeitet nebenberuflich als Privatdetektiv. Was tut sie diese Nacht?",
        7: "Die Seherin leidet unter Schlafstörungen. Was wird sie diese Nacht unternehmen?",
        8: "Die Seherin ist leidenschaftliche Spannerin. Wen stalkt sie diese Nacht?",
        9: "Die Seherin kann mal wieder nicht schlafen. Was tut sie diese Nacht?"
    }
    return switcher[gameData.randrange(0, 10)]


def seherinOptions(name, gameData):
    switcher = {
        0: name + " einsehen",
        1: name + " von der Gestapo überwachen lassen",
        2: "Informationen über " + name + " beim BND einholen",
        3: name + " bespitzeln",
        4: name + " beobachten",
        5: "Ein Auge auf " + name + " werfen",
        6: name + " ausspionieren"
    }
    option = gameData.randrange(0, 7)
    return option, switcher[option]


def seherinWerwolf(option, name):
    switcher = {
        0: name + " gehört zu den Werwölfen.",
        1: "Die Gestapo hat herausgefunden: " + name + " ist ein Werwolf.",
        2: "Der BND steckt dir zu: " + name + " ist böse!",
        3: name + " ist böse.",
        4: "Es stellt sich heraus: " + name + " gehört den Bösen an.",
        5: "Du siehst es mit deinen eigenen Augen: " + name
           + " verwandelt sich Nachts in einen Werwolf!",
        6: "Deine Ermittlungen haben ergeben: " + name + " ist ein Werwolf."
    }
    return switcher[option]


def seherinNoWerwolf(option, name):
    switcher = {
        0: name + " gehört nicht zu den Werwölfen.",
        1: "Die Gestapo hat herausgefunden: " + name + " ist kein Werwolf.",
        2: "Der BND steckt dir zu: " + name + " ist gut!",
        3: name + " ist gut.",
        4: "Es stellt sich heraus: " + name + " gehört den Guten an.",
        5: "Du siehst es mit deinen eigenen Augen: " + name
           + " verwandelt sich Nachts nicht in einen Werwolf!",
        6: "Deine Ermittlungen haben ergeben: " + name + " ist kein Werwolf."
    }
    return switcher[option]
