from src.main.server import Factory
from src.main.server.characters.Character import Character
from src.main.server.characters.Types import CharacterType
from src.main.server.characters.Types import TeamType


class Wolfshund(Character):
    def __init__(self, alive=True):
        super(Wolfshund, self).__init__(None, CharacterType.WOLFSHUND, alive)
        self.descriptions = {
            0: ("Du bist der Wolfshund. Als dieser darfst du in der ersten Nacht entscheiden, "
                "ob du das Spiel als Werwolf oder als Dorfbewohner spielen willst."),
            1: ("Du bist ein Wolfshund, welcher sowohl die Gene eines friedlichen Hundes "
                "als auch die eines Wolfes in sich hat. Er entscheidet sich in der ersten Nacht, "
                "ob er zum Dorf oder zu den Werwölfen gehören will."),
            2: ("Deine Rolle ist der Wolfshund. Der Wolfshund entscheidet sich in der ersten "
                "Nacht, ob er zu den Dorfbewohnern oder zu den Werwölfen gehören will."),
            3: ("Dein Charakter ist der Wolfshund, welcher in der ersten Nacht vor den "
                "Werwölfen erwacht und sich entscheiden muss, ob er zu den Werwölfen "
                "oder zum Dorf gehört."),
            4: ("Du bist der Wolfshund. Der Wolfshund hat die Wahl, ob er das Spiel als Werwolf "
                "oder Dorfbewohner bestreiten will."),
            5: ("Du bist der Wolfshund und besitzt die Fähigkeit, dich zu Beginn des Spieles "
                "zu entscheiden, ob du ein Dorfbewohner oder ein Werwolf wirst.")
        }

    def getDescription(self, gameData):
        return self.descriptions.get(gameData.randrange(0, 5))

    def wakeUp(self, gameData, playerId):
        if self.getTeam() is not None:
            return
        intro = wolfshundOptions(gameData)
        indexWerwolf, optionWerwolf = wolfshundChooseWerwolf(gameData)
        indexDorf, optionDorf = wolfshundChooseDorf(gameData)
        gameData.sendJSON(
            Factory.createChoiceFieldEvent(playerId, intro, [optionWerwolf, optionDorf]))
        messageId = gameData.getNextMessage(commandType="feedback")["feedback"]["messageId"]

        rec = gameData.getNextMessage(commandType="reply", fromId=playerId)
        gameData.sendJSON(
            Factory.createMessageEvent(playerId, intro, messageId, Factory.EditMode.EDIT))
        if rec["reply"]["choiceIndex"] == 0:
            self.setTeam(TeamType.WERWOLF)
            gameData.sendJSON(
                Factory.createMessageEvent(playerId, wolfshundDidChooseWerwolf(indexWerwolf)))
        elif rec["reply"]["choiceIndex"] == 1:
            self.setTeam(TeamType.VILLAGER)
            gameData.sendJSON(
                Factory.createMessageEvent(playerId, wolfshundDidChooseDorf(indexDorf)))
        else:
            raise ValueError("How can u choose option " + rec["reply"]["choiceIndex"])
        gameData.dumpNextMessage(commandType="feedback")


def wolfshundOptions(gameData):
    switcher = {
        0: "Wie möchtest du dieses Spiel bestreiten?",
        1: "Welchem Team möchtest du angehören?",
        2: "Welche Gene setzen sich in dir durch?",
        3: "Du kommst jetzt in ein Alter, in dem du dich für eine Seite entscheiden mussst.",
        4: "Wie willst du den Rest deines Lebens verbringen?",
        5: "Möchtest du Menschen fressen oder von Menschen gelyncht werden?",
        6: "Es ist an der Zeit, sich für eine Seite zu entscheiden!"
    }
    return switcher[gameData.randrange(0, 7)]


def wolfshundChooseWerwolf(gameData):
    switcher = {
        0: "in einen Werwolf verwandeln",
        1: "zum Werwolf mutieren",
        2: "das Tier in dir vorkommen lassen",
        3: "Blutlust entwickeln",
        4: "Hunger auf Menschfleisch bekommen",
        5: "dem Dorf den Rücken zuwenden",
        6: "sich den Werwölfen anschließen"
    }
    option = gameData.randrange(0, 7)
    return option, switcher[option]


def wolfshundDidChooseWerwolf(option):
    switcher = {
        0: "Du hast dich in einen Werwolf verwandelt.",
        1: "Du bist zu einem Werwolf mutiert.",
        2: "Du hast das Tier in dir durchkommen lassen.",
        3: "Du hast Blutlust enwickelt.",
        4: "Du hast Hunger auf Menschfleisch bekommen.",
        5: "Du hast dem Dorf den Rücken zugewendet.",
        6: "Du hast dich den Werwölfen angeschlossen."
    }
    return switcher[option]


def wolfshundChooseDorf(gameData):
    switcher = {
        0: "sich dem Dorf anschließen",
        1: "brav im Dorf leben",
        2: "harmloser Schoßhund werden",
        3: "doch lieber Vegetarier werden",
        4: "Wenn du Blut siehst, wird dir schlecht",
        5: "Demokratie der Gewalt vorziehen",
        6: "Humanität zeigen"
    }
    option = gameData.randrange(0, 7)
    return option, switcher[option]


def wolfshundDidChooseDorf(option):
    switcher = {
        0: "Du hast dich dem Dorf angeschlossen.",
        1: "Du lebst von nun an brav im Dorf.",
        2: "Du bist zu einem harmlosen Schoßhund geworden.",
        3: "Du hast beschlossen, doch lieber Vegetarier zu werden.",
        4: "Du hast Hämatophobie.",
        5: "Du ziehst die Demokratie der Gewalt vor.",
        6: "Du zeigst Humanität."
    }
    return switcher[option]
