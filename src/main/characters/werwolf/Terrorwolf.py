import random

from ..Types import CharacterType
from ..Teams import WerwolfTeam

from ... import Factory


class Terrorwolf(WerwolfTeam):
    def __init__(self, isAlive=True):
        super(Terrorwolf, self).__init__(CharacterType.TERRORWOLF, isAlive)
        self.descriptions = {
            0: """Du bist der Terrorwolf. Wenn der Terrorwolf stirbt, nimmt er noch \
            einen Spieler seiner Wahl mit in den Tod.""",
            1: """Du bist der Terrorwolf. Der Terrorwolf ist der Jäger der Werwölfe: \
            Sollte er sterben, kann er noch einen Charakter seiner Wahl mit in den Tod reißen.""",
            2: """Dein Carakter ist der Terrorwolf, welcher, sollte er zu Tode kommen, \
            in letzter Sekunde noch ein Opfer reißen kann.""",
            3: """Du bist der Terrorwolf. Dieser ist ähnlich dem Jäger, mit dem Unterschied, \
            dass er für die Werwölfe spielt: Stirbt der Terrorwolf, egal ob bei Tag oder Nacht, \
            so bleibt ihm noch ausreichend Zeit, sich einen Dorfbewohner als \
            Henkersmahlzeit zu schnappen.""",
            4: """Deine Rolle ist er Terrorwolf, welcher mittels eines Testaments \
            den Tod eines Dorfbewohners einfordert.""",
            5: """Du bist der Terrorwolf. Dein Tod hat Konsequenzen. Zumindest für einen weiteren \
            Dorfbewohner: Wenn du stirbst, steht er als letzte Mahlzeit auf deinem Speiseplan."""
        }

    def getDescription(self):
        return self.descriptions.get(random.randrange(0, 5))

    def kill(self, gameData, playerId, dm=None):
        super(Terrorwolf, self).kill(gameData, playerId)
        gameData.sendJSON(Factory.createMessageEvent(gameData.getOrigin(),
                                                     gameData.getPlayers()[
                                                         playerId].getName() + terrorwolf_reveal()))
        gameData.dumpNextMessageDict()

        options = []
        for player in gameData.getAlivePlayers():
            options.append(player.getName())

        text = terrorwolf_choose_target()
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessageDict()["feedback"]["messageId"]

        rec = gameData.getNextMessageDict()
        gameData.sendJSON(Factory.createMessageEvent(
            playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessageDict()

        target = gameData.getAlivePlayers()[rec["reply"]["choiceIndex"]]

        gameData.getAlivePlayers()[target].kill(gameData, target)


def terrorwolf_reveal():
    desc_no = random.randrange(0, 10)
    if desc_no == 0:
        return " war der Terrorwolf!"
    elif desc_no == 1:
        return " will noch jemanden in seinem Testament zerfleischen lassen."
    elif desc_no == 2:
        return " reißt sein Maul auf: Ihm bleibt noch genügend Zeit, jemanden zu fressen"
    elif desc_no == 3:
        return " beißt einen Dorfbewohner!"
    elif desc_no == 4:
        return " will seinen Freunden mit seinem Tod helfen und sucht sich eine Henkersmahlzeit."
    elif desc_no == 5:
        return " kriegt vor seinem Tod nochmal Hunger."
    elif desc_no == 6:
        return " will im Sterben noch jemanden versnacken!"
    elif desc_no == 7:
        return " will nicht alleine sterben und fletscht die Zähne."
    elif desc_no == 8:
        return " genießt es, jemanden zu sehen - und zerfetzt ihn!"
    else:
        return " fordert sein Recht ein - vor dem Tod noch ein letztes Mal Beute fangen."


def terrorwolf_choose_target():
    desc_no = random.randrange(0, 10)
    if desc_no == 0:
        return "Wen möchtest du mit ins Grab nehmen?"
    elif desc_no == 1:
        return "Wen möchtest du zerfleischen?"
    elif desc_no == 2:
        return "Wen willst du versnacken?"
    elif desc_no == 3:
        return "Wen willst du in Notwehr zerfetzen?"
    elif desc_no == 4:
        return "Wen willst du 'ausversehen' mit deinen Zähnen füllen?"
    elif desc_no == 5:
        return "Wem möchtest du wortwörtlich den Kopf abreißen?"
    elif desc_no == 6:
        return "Wem möchtest du dazu verhelfen, an inneren Blutungen zu erliegen?"
    elif desc_no == 7:
        return "Wen willst du als letzten Akt zerreißen?"
    elif desc_no == 8:
        return "Wem gönnst du es nicht, ohne dich weiterzuleben?"
    else:
        return "Wer soll durch deine Krallen seine ewige Ruhe finden?"
