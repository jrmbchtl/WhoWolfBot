from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType


class Hunter(VillagerTeam):
    def __init__(self, alive=True):
        super(Hunter, self).__init__(CharacterType.HUNTER, "hunterDescription", alive)

    def kill(self, gameData, playerId, dm=None):
        super(Hunter, self).kill(gameData, playerId, dm)
        announcement = gameData.getPlayers()[playerId].getName() + gameData.getMessage(
            "hunterReveal", rndm=True)
        gameData.sendJSON(Factory.createMessageEvent(gameData.getOrigin(), announcement))
        gameData.dumpNextMessage(commandType="feedback", fromId=gameData.getOrigin())
        text = gameData.getMessage("hunterQuestion", rndm=True)
        options = []
        idToChoice = {}
        idList = []
        for player in gameData.getAlivePlayerList():
            if player == gameData.getWerewolfTarget() or player == gameData.getWitchTarget():
                continue
            name = gameData.getPlayers()[player].getName()
            choice, message = gameData.getMessagePrePost(
                "hunterOptions", name, rndm=True, retOpt=True)
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
        dm += gameData.getMessage("hunterShot", option=idToChoice[targetId])
        gameData.getPlayers()[targetId].getCharacter().kill(gameData, targetId, dm)
