from ..Types import CharacterType
from ..Teams import VillagerTeam
from ... import Factory


class Jaeger(VillagerTeam):
    def __init__(self, isAlive=True):
        super(Jaeger, self).__init__(CharacterType.JAEGER, isAlive)
        self.descriptions = {
            0: """Du bist der Jäger: Sollte er zu Tode kommen, kann er einen letzten Schuss \
            abgeben und einen Mitspieler mit ins Verderben reißen.""",
            1: """Du bist der Jäger, welcher in seinem letzen Atemzug noch zum Gewehr greift, \
            um einen beliebigen Mitspieler ins Jenseits zu befördern.""",
            2: """Bei deinem Charakter handelt es sich um den Jäger, welcher als letzte Aktion \
            vor seinem Tod noch einen Spieler erschießen muss.""",
            3: """Du bist der Jäger. Wenn der Jäger stirbt, muss er noch einen Spieler seiner \
            Wahl in den Tod mitnehmen.""",
            4: """Du bist der Jäger. Scheidet der Jäger aus dem Spiel aus, feuert er in seinem \
            letzten Atemzug noch einen Schuss ab, mit dem er einen Spieler seiner \
            Wahl mit in den Tod reißt.""",
            5: """Du bist der Jäger. Als dieser musst du direkt vor deinem Tod mit deiner Jagdwaffe \
            einen anderen Bewohner des Dorfes erschießen."""
        }

    def getDescription(self, gameData):
        return self.descriptions.get(gameData.randrange(0, 6))

    def kill(self, gameData, playerId, dm=None):
        super(Jaeger, self).kill(gameData, playerId, dm)
        announcement = gameData.getPlayers()[playerId].getName() + jaegerReveal(gameData)
        gameData.sendJSON(Factory.createMessageEvent(gameData.getOrigin(), announcement))
        gameData.dumpNextMessageDict()
        text = jaegerChooseTarget(gameData)
        options = []
        idToChoice = {}
        for player in gameData.getAlivePlayerList():
            choice, message = jaegerOptions(gameData)
            idToChoice[player] = choice
            options.append(gameData.getPlayers()[player].getName() + message)

        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessageDict()["feedback"]["messageId"]

        rec = gameData.getNextMessageDict()
        gameData.sendJSON(Factory.createMessageEvent(
            playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessageDict()

        targetId = gameData.getAlivePlayerList()[rec["reply"]["choiceIndex"]]

        dm = gameData.getPlayers()[targetId]
        dm += jaegerShot(idToChoice[targetId])
        gameData.getPlayers()[targetId].getCharacter().kill(gameData, targetId, dm)


def jaegerReveal(gameData):
    switcher = {
        0: " war der Jäger!",
        1: " schießt rücksichtslos, um nicht alleine sterben zu müssen!",
        2: " trägt eine geladene Waffe bei sich!",
        3: " zückt eine Schrotflinte!",
        4: " versucht mit Waffengewalt, kurz vor seinem Tod noch für Gerechtigkeit zu sorgen!",
        5: " hat einen Jagdschein!",
        6: " hat eine Jagdlizenz. Jetzt auch für Menschen!",
        7: " will nicht alleine sterben und zieht einen Revolver!",
        8: " genießt es, jemanden zu sehen - und erschießt ihn!",
        9: " fordert sein Recht ein - jemanden mit Waffengewalt in den Tod mitzunehmen.",
        10: " hat die Flinte noch nicht ins Korn geworfen!"
    }
    return switcher[gameData.randrange(0, 11)]


def jaegerChooseTarget(gameData):
    switcher = {
        0: "Wen möchtest du mit ins Grab nehmen?",
        1: "Wen möchtest du erschießen?",
        2: "Wen willst du wegpusten?",
        3: "Wen willst du in Notwehr abknallen?",
        4: "Wen willst du ausversehen mit 15 Schüssen in der Brust treffen?",
        5: "Wen möchtest du mit Blei ausstopfen?",
        6: "Wem möchtest du zu einer inneren Bleivergiftung verhelfen?",
        7: "Wen willst du als letzten Akt erschießen?",
        8: "Wem gönnst du es nicht, ohne dich weiterzuleben?",
        9: "Wer soll im Kugelhagel seine ewige Ruhe finden?",
        10: "Wen willst du in Mitleidenschaft ziehen?"
    }
    return switcher[gameData.randrange(0, 11)]


def jaegerOptions(gameData):
    switcher = {
        0: " erschießen",
        1: " mit der Nagelpistole an die Wand heften",
        2: " durchlöchern",
        3: " umlegen",
        4: " wegpusten",
        5: " in der Notwehr erschießen",
        6: " niederstrecken",
        7: " zur Jagdtrophäe befördern",
        8: " mit in den Tod reißen",
        9: " einen Gnadenschuss verpassen"
    }
    choice = gameData.randrange(0, 10)
    return choice, switcher[choice]


def jaegerShot(option):
    switcher = {
        0: " wurde vom Jäger erschossen.",
        1: " wurde mit einer Nagelpistole an die Wand geheftet!",
        2: " hat nun sehr viele Löcher in Kopf und Brust.",
        3: " wurde umgelegt.",
        4: " hat sich wegpusten lassen.",
        5: " wurde in der Notwehr des Jägers erschossen!",
        6: " wurde niedergestreckt.",
        7: " endete als letzte Jagdtrophäe des Jägers!",
        8: " wurde vom Jäger mit in den Tod gerissen.",
        9: " hat einen Gnadenschuss erhalten."
    }
    return switcher[option]
