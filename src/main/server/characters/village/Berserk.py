from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc


class Berserk(VillagerTeam):
    def __init__(self, alive=True):
        super(Berserk, self).__init__(CharacterType.BERSERK, alive)
        self.lives = 2

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "berserkDescription")
        return dc[str(gameData.randrange(0, len(dc)))]

    def wakeUp(self, gameData, playerId):
        if self.lives == 2:
            text = loc(gameData.getLang(), "berserkTwoLives")
        else:
            text = loc(gameData.getLang(), "berserkOneLive")
        option, question = berserkQuestion(gameData)
        text += question
        options = []
        players = gameData.getAlivePlayers()
        for p in players:
            options.append(players[p].getName())
        options.append(loc(gameData.getLang(), "noone"))
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessage("feedback", playerId)

        choice = gameData.getNextMessage("reply", playerId)["reply"]["choiceIndex"]
        text += "\n\n" + berserkResponse(gameData, options[choice], option)
        gameData.sendJSON(Factory.createMessageEvent(
            playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage("feedback", playerId)

        gameData.setBerserkTarget(None)
        if choice < len(players):
            self.lives -= 1
            gameData.addBerserkTarget(gameData.getAlivePlayerList()[choice])
            if self.lives <= 0:
                gameData.addBerserkTarget(playerId)

    def werewolfKillAttempt(self):
        self.lives -= 1
        if self.lives <= 0:
            return True
        else:
            return False


def berserkQuestion(gameData):
    dc = loc(gameData.getLang(), "berserkQuestion")
    option = gameData.randrange(0, len(dc))
    return option, dc[str(option)]


def berserkResponse(gameData, name, option):
    pre = loc(gameData.getLang(), "berserkResponsePre", option)
    post = loc(gameData.getLang(), "berserkResponsePost", option)
    return pre + name + post
