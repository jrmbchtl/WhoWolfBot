from src.main.server import Factory
from src.main.server.characters.Teams import WerewolfTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc


class Terrorwolf(WerewolfTeam):
    def __init__(self, alive=True):
        super(Terrorwolf, self).__init__(CharacterType.TERRORWOLF, alive)

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "seerDescription")
        return dc[str(gameData.randrange(0, len(dc)))]

    def kill(self, gameData, playerId, dm=None):
        super(Terrorwolf, self).kill(gameData, playerId)
        gameData.sendJSON(
            Factory.createMessageEvent(gameData.getOrigin(),
                                       gameData.getPlayers()[playerId].getName()
                                       + terrorwolfReveal(gameData)))
        gameData.dumpNextMessage(commandType="feedback", fromId=gameData.getOrigin())

        options = []
        for player in gameData.getAlivePlayers():
            options.append(gameData.getAlivePlayers()[player].getName())

        text = terrorwolfChooseTarget(gameData)
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessage(
            commandType="feedback", fromId=playerId)["feedback"]["messageId"]

        rec = gameData.getNextMessage(commandType="reply", fromId=playerId)
        gameData.sendJSON(Factory.createMessageEvent(
            playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)

        targetId = gameData.getAlivePlayerList()[rec["reply"]["choiceIndex"]]

        gameData.getAlivePlayers()[targetId].getCharacter() \
            .kill(gameData, targetId,
                  gameData.getAlivePlayers()[targetId].getName() + terrorwolfKill(gameData))


def terrorwolfReveal(gameData):
    dc = loc(gameData.getLang(), "terrorwolfReveal")
    return dc[str(gameData.randrange(0, len(dc)))]


def terrorwolfChooseTarget(gameData):
    dc = loc(gameData.getLang(), "terrorwolfQuestion")
    return dc[str(gameData.randrange(0, len(dc)))]


def terrorwolfKill(gameData):
    dc = loc(gameData.getLang(), "terrorwolfKill")
    return dc[str(gameData.randrange(0, len(dc)))]
