from src.main.server import Factory
from src.main.server.Factory import EditMode
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType


class Psychopath(VillagerTeam):
    def __init__(self, alive=True):
        super(Psychopath, self).__init__(CharacterType.PSYCHOPATH, "psychopathDescription", alive)

    def wakeUp(self, gameData, playerId):
        if len(gameData.getNightlyTarget()) == 0:
            text = gameData.getMessage("psychopathQuestion", rndm=True)
            options = []
            idToChoice = {}
            for p in gameData.getAlivePlayers():
                name = gameData.getAlivePlayers()[p].getName()
                choice, message = gameData.getMessagePrePost(
                    "psychopathOption", name, rndm=True, retOpt=True)
                options.append(message)
                idToChoice[p] = choice

            gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
            messageId = gameData.getNextMessage("feedback", playerId)["feedback"]["messageId"]

            choice = gameData.getNextMessage("reply", playerId)["reply"]["choiceIndex"]
            targetId = gameData.getAlivePlayerList()[choice]
            name = gameData.getAlivePlayers()[targetId].getName()
            text += "\n\n" + gameData.getMessagePrePost(
                "psychopathResponse", name, option=idToChoice[targetId])

            gameData.sendJSON(Factory.createMessageEvent(playerId, text, messageId, EditMode.EDIT))
            gameData.dumpNextMessage("feedback", playerId)

            gameData.setNightlyTarget(targetId, CharacterType.PSYCHOPATH)
