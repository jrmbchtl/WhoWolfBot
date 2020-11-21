from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.server.characters.Types import TeamType
from src.main.localization import getLocalization as loc


class Seer(VillagerTeam):
    def __init__(self, alive=True):
        super(Seer, self).__init__(CharacterType.SEER, alive)

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "seerDescription")
        return dc[str(gameData.randrange(0, len(dc)))]

    def wakeUp(self, gameData, playerId):
        options = []
        playerIndexList = []
        playerToOption = {}
        for player in gameData.getAlivePlayers():
            if player != playerId:
                option, text = \
                    seerOptions(gameData.getAlivePlayers()[player].getName(), gameData)
                options.append(text)
                playerToOption[player] = option
                playerIndexList.append(player)
        text = seerChooseTarget(gameData)
        gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
        messageId = gameData.getNextMessage(
            commandType="feedback", fromId=playerId)["feedback"]["messageId"]

        choice = gameData.getNextMessage(
            commandType="reply", fromId=playerId)["reply"]["choiceIndex"]

        gameData.sendJSON(
            Factory.createMessageEvent(playerId, text, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)

        if gameData.getAlivePlayers()[playerIndexList[choice]].\
                getCharacter().getTeam() == TeamType.WEREWOLF:
            replyText = seerWerewolf(gameData, choice,
                                     gameData.getAlivePlayers()[playerIndexList[choice]].getName())
        else:
            replyText = seerNoWerewolf(gameData, choice,
                                       gameData.getAlivePlayers()[playerIndexList[choice]]
                                       .getName())
        gameData.sendJSON(Factory.createMessageEvent(playerId, replyText))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)


def seerChooseTarget(gameData):
    dc = loc(gameData.getLang(), "seerQuestion")
    return dc[str(gameData.randrange(0, len(dc)))]


def seerOptions(name, gameData):
    pre = loc(gameData.getLang(), "seerOptionsPre")
    post = loc(gameData.getLang(), "seerOptionsPost")
    option = gameData.randrange(0, 7)
    return option, pre[str(option)] + name + post[str(option)]


def seerWerewolf(gameData, option, name):
    pre = loc(gameData.getLang(), "seerWerewolfPre", option)
    post = loc(gameData.getLang(), "seerWerewolfPost", option)
    return pre + name + post


def seerNoWerewolf(gameData, option, name):
    pre = loc(gameData.getLang(), "seerNoWerewolfPre", option)
    post = loc(gameData.getLang(), "seerNoWerewolfPost", option)
    return pre + name + post
