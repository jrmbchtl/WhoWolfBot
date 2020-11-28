from src.main.server import Factory
from src.main.server.characters.Teams import WhitewolfTeam
from src.main.server.characters.Types import CharacterType
from src.main.server.characters.Types import TeamType
from src.main.localization import getLocalization as loc


class Whitewolf(WhitewolfTeam):
    def __init__(self, alive=True):
        super(Whitewolf, self).__init__(CharacterType.WHITEWOLF, "whitewolfDescription", alive)
        self.dontWake = False

    def wakeUp(self, gameData, playerId):
        if self.dontWake:
            self.dontWake = False
            return
        else:
            self.dontWake = True
        wwList = []
        players = gameData.getAlivePlayers()
        for p in players:
            if players[p].getCharacter().getTeam() == TeamType.WEREWOLF:
                wwList.append(p)
        options = []
        if len(wwList) == 0:
            return
        for w in wwList:
            player = gameData.getAlivePlayers()[w]
            options.append(player.getName())
        options.append(loc(gameData.getLang(), "Noone"))
        text = gameData.getMessage("whitewolfQuestion", rndm=True)
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessage("feedback", playerId)

        rec = gameData.getNextMessage("reply", playerId)
        choice = rec["reply"]["choiceIndex"]
        targetName = loc(gameData.getLang(), "Noone")
        if choice < len(wwList):
            targetId = wwList[choice]
            gameData.setNightlyTarget(targetId, CharacterType.WHITEWOLF)
            targetName = gameData.getAlivePlayers()[targetId].getName()
        text += "\n" + targetName
        gameData.sendJSON(
            Factory.createMessageEvent(playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage("feedback", playerId)
