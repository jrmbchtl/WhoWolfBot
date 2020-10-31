from src.main.server import Factory
from src.main.server.characters.Teams import WerwolfTeam
from src.main.server.characters.Types import CharacterType


class Terrorwolf(WerwolfTeam):
    def __init__(self, alive=True):
        super(Terrorwolf, self).__init__(CharacterType.TERRORWOLF, alive)
        self.descriptions = {
            0: ("Du bist der Terrorwolf. Wenn der Terrorwolf stirbt, nimmt er noch "
                "einen Spieler seiner Wahl mit in den Tod."),
            1: ("Du bist der Terrorwolf. Der Terrorwolf ist der Jäger der Werwölfe: "
                "Sollte er sterben, kann er noch einen Charakter seiner Wahl mit in den Tod "
                "reißen."),
            2: ("Dein Carakter ist der Terrorwolf, welcher, sollte er zu Tode kommen, "
                "in letzter Sekunde noch ein Opfer reißen kann."),
            3: ("Du bist der Terrorwolf. Dieser ist ähnlich dem Jäger, mit dem Unterschied, "
                "dass er für die Werwölfe spielt: Stirbt der Terrorwolf, egal ob bei Tag oder "
                "Nacht, so bleibt ihm noch ausreichend Zeit, sich einen Dorfbewohner als "
                "Henkersmahlzeit zu schnappen."),
            4: ("Deine Rolle ist er Terrorwolf, welcher mittels eines Testaments "
                "den Tod eines Dorfbewohners einfordert."),
            5: ("Du bist der Terrorwolf. Dein Tod hat Konsequenzen. Zumindest für einen weiteren "
                "Dorfbewohner: Wenn du stirbst, steht er als letzte Mahlzeit auf deinem "
                "Speiseplan.")
        }

    def getDescription(self, gameData):
        return self.descriptions.get(gameData.randrange(0, 5))

    def kill(self, gameData, playerId, dm=None):
        super(Terrorwolf, self).kill(gameData, playerId)
        gameData.sendJSON(
            Factory.createMessageEvent(gameData.getOrigin(),
                                       gameData.getPlayers()[playerId].getName()
                                       + terrorwolfReveal(gameData)))
        gameData.dumpNextMessageDict()

        options = []
        for player in gameData.getAlivePlayers():
            options.append(gameData.getAlivePlayers()[player].getName())

        text = terrorwolfChooseTarget(gameData)
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessageDict()["feedback"]["messageId"]

        rec = gameData.getNextMessageDict()
        gameData.sendJSON(Factory.createMessageEvent(
            playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessageDict()

        targetId = gameData.getAlivePlayerList()[rec["reply"]["choiceIndex"]]

        gameData.getAlivePlayers()[targetId].getCharacter() \
            .kill(gameData, targetId,
                  gameData.getAlivePlayers()[targetId].getName() + terrorwolfKill(gameData))


def terrorwolfReveal(gameData):
    switcher = {
        0: " war der Terrorwolf!",
        1: " will noch jemanden in seinem Testament zerfleischen lassen.",
        2: " reißt sein Maul auf: Ihm bleibt noch genügend Zeit, jemanden zu fressen",
        3: " beißt einen Dorfbewohner!",
        4: " will seinen Freunden mit seinem Tod helfen und sucht sich eine Henkersmahlzeit.",
        5: " kriegt vor seinem Tod nochmal Hunger.",
        6: " will im Sterben noch jemanden versnacken!",
        7: " will nicht alleine sterben und fletscht die Zähne.",
        8: " genießt es, jemanden zu sehen - und zerfetzt ihn!",
        9: " fordert sein Recht ein - vor dem Tod noch ein letztes Mal Beute fangen."
    }
    return switcher[gameData.randrange(0, 10)]


def terrorwolfChooseTarget(gameData):
    switcher = {
        0: "Wen möchtest du mit ins Grab nehmen?",
        1: "Wen möchtest du zerfleischen?",
        2: "Wen willst du versnacken?",
        3: "Wen willst du in Notwehr zerfetzen?",
        4: "Wen willst du 'ausversehen' mit deinen Zähnen füllen?",
        5: "Wem möchtest du wortwörtlich den Kopf abreißen?",
        6: "Wem möchtest du dazu verhelfen, an inneren Blutungen zu erliegen?",
        7: "Wen willst du als letzten Akt zerreißen?",
        8: "Wem gönnst du es nicht, ohne dich weiterzuleben?",
        9: "Wer soll durch deine Krallen seine ewige Ruhe finden?"
    }
    return switcher[gameData.randrange(0, 10)]


def terrorwolfKill(gameData):
    switcher = {
        0: " wurde vom Terrorwolf gerissen.",
        1: " wurde als Henkersmahlzeit verspeißt!",
        2: " wurde mit in den Tod gerissen.",
        3: " wurde noch kurz verputzt.",
        4: " hat sich im Vorbeilaufen die Zähne in den Hals rammen lassen.",
        5: " wurde mit der letzen Kraft des Terrorwolfes zerbissen.",
        6: " wurde in der Luft zerfetzt.",
        7: " wurde bei einem Attentäter in Auftrag gegeben und konnte nicht entkommen.",
        8: " kann ohne seinen Kopf nicht weiterleben!",
        9: " wurde noch kurz aus Mitleid aufgegessen."
    }
    return switcher[gameData.randrange(0, 10)]
