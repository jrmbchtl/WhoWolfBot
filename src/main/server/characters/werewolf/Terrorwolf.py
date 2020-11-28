from src.main.server import Factory
from src.main.server.characters.Teams import WerewolfTeam
from src.main.server.characters.Types import CharacterType


class Terrorwolf(WerewolfTeam):
    def __init__(self, alive=True):
        super(Terrorwolf, self).__init__(CharacterType.TERRORWOLF, "terrorwolfDescription", alive)

    def kill(self, gameData, playerId, dm=None):
        super(Terrorwolf, self).kill(gameData, playerId)
        name = gameData.getPlayers()[playerId].getName()
        text = name + gameData.getMessage("terrorwolfReveal", rndm=True)
        gameData.sendJSON(
            Factory.createMessageEvent(gameData.getOrigin(), text))
        gameData.dumpNextMessage(commandType="feedback", fromId=gameData.getOrigin())

        options = []
        for player in gameData.getAlivePlayers():
            options.append(gameData.getAlivePlayers()[player].getName())

        text = gameData.getMessage("terrorwolfQuestion", rndm=True)
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessage(
            commandType="feedback", fromId=playerId)["feedback"]["messageId"]

        rec = gameData.getNextMessage(commandType="reply", fromId=playerId)
        gameData.sendJSON(Factory.createMessageEvent(
            playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)

        targetId = gameData.getAlivePlayerList()[rec["reply"]["choiceIndex"]]
        name = gameData.getAlivePlayers()[targetId].getName()
        dm = name + gameData.getMessage("terrorwolfKill", rndm=True)
        gameData.getAlivePlayers()[targetId].getCharacter().kill(gameData, targetId, dm)
