from src.main.server import Factory
from src.main.server.characters.Character import Character
from src.main.server.characters.Types import CharacterType
from src.main.server.characters.Types import TeamType
from src.main.localization import getLocalization as loc


class Wolfdog(Character):
    def __init__(self, alive=True):
        super(Wolfdog, self).__init__(None, CharacterType.WOLFDOG, alive)

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "wolfdogDescription")
        return dc[str(gameData.randrange(0, len(dc)))]

    def wakeUp(self, gameData, playerId):
        if self.getTeam() is not None:
            return
        intro = wolfdogOptions(gameData)
        indexWerewolf, optionWerewolf = wolfdogChooseWerewolf(gameData)
        indexVillage, optionVillage = wolfdogChooseVillage(gameData)
        gameData.sendJSON(
            Factory.createChoiceFieldEvent(playerId, intro, [optionWerewolf, optionVillage]))
        messageId = gameData.getNextMessage(
            commandType="feedback", fromId=playerId)["feedback"]["messageId"]

        rec = gameData.getNextMessage(commandType="reply", fromId=playerId)
        if rec["reply"]["choiceIndex"] == 0:
            self.setTeam(TeamType.WEREWOLF)
            intro += "\n\n" + wolfdogChoseWerewolf(gameData, indexWerewolf)
        elif rec["reply"]["choiceIndex"] == 1:
            self.setTeam(TeamType.VILLAGER)
            intro += "\n\n" + wolfdogChoseVillage(gameData, indexVillage)
        else:
            raise ValueError("How can u choose option " + rec["reply"]["choiceIndex"])
        gameData.sendJSON(
            Factory.createMessageEvent(playerId, intro, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)


def wolfdogOptions(gameData):
    dc = loc(gameData.getLang(), "wolfdogQuestion")
    return dc[str(gameData.randrange(0, len(dc)))]


def wolfdogChooseWerewolf(gameData):
    dc = loc(gameData.getLang(), "wolfdogChooseWerewolf")
    option = gameData.randrange(0, len(dc))
    return option, dc[str(option)]


def wolfdogChoseWerewolf(gameData, option):
    return loc(gameData.getLang(), "wolfdogChoseWerewolf", option)


def wolfdogChooseVillage(gameData):
    dc = loc(gameData.getLang(), "wolfdogChooseVillage")
    option = gameData.randrange(0, len(dc))
    return option, dc[str(option)]


def wolfdogChoseVillage(gameData, option):
    return loc(gameData.getLang(), "wolfdogChoseVillage", option)
