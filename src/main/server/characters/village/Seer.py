from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.server.characters.Types import TeamType


class Seer(VillagerTeam):
    def __init__(self, alive=True):
        super(Seer, self).__init__(CharacterType.SEER, "seerDescription", alive)

    def wakeUp(self, gameData, playerId):
        options = []
        playerIndexList = []
        playerToOption = {}
        for player in gameData.getAlivePlayers():
            if player != playerId:
                name = gameData.getAlivePlayers()[player].getName()
                option, text = gameData.getMessagePrePost(
                    "seerOptions", name, rndm=True, retOpt=True)
                options.append(text)
                playerToOption[player] = option
                playerIndexList.append(player)
        text = gameData.getMessage("seerQuestion", rndm=True)
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessage(
            commandType="feedback", fromId=playerId)["feedback"]["messageId"]

        choice = gameData.getNextMessage(
            commandType="reply", fromId=playerId)["reply"]["choiceIndex"]

        gameData.sendJSON(
            Factory.createMessageEvent(playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)

        name = gameData.getAlivePlayers()[playerIndexList[choice]].getName()
        if gameData.getAlivePlayers()[playerIndexList[choice]].\
                getCharacter().getTeam() == TeamType.WEREWOLF:
            replyText = gameData.getMessagePrePost("seerWerewolf", name, option=choice)
        else:
            replyText = gameData.getMessagePrePost("seerNoWerewolf", name, option=choice)
        gameData.sendJSON(Factory.createMessageEvent(playerId, replyText))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)
