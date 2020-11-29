from src.main.server import Factory
from src.main.server.Factory import EditMode
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType


class Scallywag(VillagerTeam):
    def __init__(self, alive=True):
        super(Scallywag, self).__init__(CharacterType.SCALLYWAG, "scallywagDescription", alive)
        self.secondLive = True
        self.bombOwner = None

    def wakeUp(self, gameData, playerId):
        if self.bombOwner is None:
            o, text = gameData.getMessage("scallywagQuestion", rndm=True, retOpt=True)
            options = []
            for p in gameData.getAlivePlayers():
                options.append(gameData.getAlivePlayers()[p].getName())
            gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
            messageId = gameData.getNextMessage("feedback", playerId)["feedback"]["messageId"]

            choice = gameData.getNextMessage("reply", playerId)["reply"]["choiceIndex"]
            targetId = gameData.getAlivePlayerList()[choice]
            self.bombOwner = targetId
            print(self.bombOwner)
            name = gameData.getAlivePlayers()[targetId].getName()
            text += "\n\n" + gameData.getMessagePrePost("scallywagResponse", name, o)
            gameData.sendJSON(Factory.createMessageEvent(playerId, text, messageId, EditMode.EDIT))
            gameData.dumpNextMessage("feedback", playerId)
        else:
            i = gameData.getPlayerList().index(self.bombOwner)
            while True:
                i += 1
                if i >= len(gameData.getPlayerList()):
                    i = 0
                if gameData.getPlayerList()[i] in gameData.getAlivePlayers():
                    self.bombOwner = gameData.getPlayerList()[i]
                    print(self.bombOwner)
                    break

    def kill(self, gameData, playerId, dm=None):
        super(Scallywag, self).kill(gameData, playerId, dm)
        if self.bombOwner in gameData.getAlivePlayerList():
            target = gameData.getAlivePlayers()[self.bombOwner].getCharacter()
            target.kill(gameData, self.bombOwner)
