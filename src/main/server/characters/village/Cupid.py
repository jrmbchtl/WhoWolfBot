from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc


class Cupid(VillagerTeam):
    def __init__(self, alive=True):
        super(Cupid, self).__init__(CharacterType.CUPID, alive)
        self.wasWaked = False

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "cupidDescription")
        return dc[str(gameData.randrange(0, len(dc)))]

    def wakeUp(self, gameData, playerId):
        if self.wasWaked:
            return
        else:
            self.wasWaked = True
        text = cupidQuestion(gameData)
        options = []
        optionId = []
        playerList = gameData.getAlivePlayerList()
        players = gameData.getAlivePlayers()
        andS = loc(gameData.getLang(), "and")
        for i in range(0, len(players)):
            ip = playerList[i]
            for j in range(i + 1, len(players)):
                jp = playerList[j]
                options.append(players[ip].getName() + " " + andS + " " + players[jp].getName())
                optionId.append([ip, jp])
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessage("feedback", playerId)

        choice = gameData.getNextMessage("reply", playerId)["reply"]["choiceIndex"]
        text += "\n\n" + options[choice]
        gameData.sendJSON(Factory.createMessageEvent(
            playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage("feedback", playerId)

        for i in optionId[choice]:
            if optionId[choice][0] == i:
                belovedName = players[optionId[choice][1]].getName()
                players[optionId[choice][0]].getCharacter().setBeloved(optionId[choice][1])
            else:
                belovedName = players[optionId[choice][0]].getName()
                players[optionId[choice][1]].getCharacter().setBeloved(optionId[choice][0])
            text = fellInLove(gameData, belovedName)
            gameData.sendJSON(Factory.createMessageEvent(i, text))
            gameData.dumpNextMessage("feedback", i)


def cupidQuestion(gameData):
    dc = loc(gameData.getLang(), "cupidQuestion")
    return dc[str(gameData.randrange(0, len(dc)))]


def fellInLove(gameData, name):
    pre = loc(gameData.getLang(), "fellInLovePre")
    post = loc(gameData.getLang(), "fellInLovePost")
    return pre + name + post
