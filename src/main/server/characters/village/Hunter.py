from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc


class Hunter(VillagerTeam):
    def __init__(self, alive=True):
        super(Hunter, self).__init__(CharacterType.HUNTER, alive)

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "hunterDescription")
        return dc[str(gameData.randrange(0, len(dc)))]

    def kill(self, gameData, playerId, dm=None):
        super(Hunter, self).kill(gameData, playerId, dm)
        announcement = gameData.getPlayers()[playerId].getName() + hunterReveal(gameData)
        gameData.sendJSON(Factory.createMessageEvent(gameData.getOrigin(), announcement))
        gameData.dumpNextMessage(commandType="feedback", fromId=gameData.getOrigin())
        text = hunterChooseTarget(gameData)
        options = []
        idToChoice = {}
        idList = []
        for player in gameData.getAlivePlayerList():
            if player == gameData.getWerewolfTarget() or player == gameData.getWitchTarget():
                continue
            name = gameData.getPlayers()[player].getName()
            choice, message = hunterOptions(gameData, name)
            idList.append(player)
            idToChoice[player] = choice
            options.append(message)

        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessage(
            commandType="feedback", fromId=playerId)["feedback"]["messageId"]

        rec = gameData.getNextMessage(commandType="reply", fromId=playerId)
        gameData.sendJSON(Factory.createMessageEvent(
            playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)

        targetId = idList[rec["reply"]["choiceIndex"]]
        dm = gameData.getPlayers()[targetId].getName()
        dm += hunterShot(gameData, idToChoice[targetId])
        gameData.getPlayers()[targetId].getCharacter().kill(gameData, targetId, dm)


def hunterReveal(gameData):
    dc = loc(gameData.getLang(), "hunterReveal")
    return dc[str(gameData.randrange(0, len(dc)))]


def hunterChooseTarget(gameData):
    dc = loc(gameData.getLang(), "hunterQuestion")
    return dc[str(gameData.randrange(0, len(dc)))]


def hunterOptions(gameData, name):
    pre = loc(gameData.getLang(), "hunterOptionsPre")
    post = loc(gameData.getLang(), "hunterOptionsPost")
    option = gameData.randrange(0, len(pre))
    return option, pre[str(option)] + name + post[str(option)]


def hunterShot(gameData, option):
    return loc(gameData.getLang(), "hunterShot", option)
