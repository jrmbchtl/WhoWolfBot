from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.server.characters.Types import TeamType
from src.main.localization import getLocalization as loc

lang = "DE"


class Seer(VillagerTeam):
    def __init__(self, alive=True):
        super(Seer, self).__init__(CharacterType.SEER, alive)

    def getDescription(self, gameData):
        dc = loc(lang, "seerDescription")
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
            replyText = seerWerewolf(choice, gameData.getAlivePlayers()[playerIndexList[choice]]
                                     .getName())
        else:
            replyText = seerNoWerewolf(choice, gameData.getAlivePlayers()[playerIndexList[choice]]
                                       .getName())
        gameData.sendJSON(Factory.createMessageEvent(playerId, replyText))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)


def seerChooseTarget(gameData):
    dc = loc(lang, "seerQuestion")
    return dc[str(gameData.randrange(0, len(dc)))]


def seerOptions(name, gameData):
    pre = loc(lang, "seerOptionsPre")
    post = loc(lang, "seerOptionsPost")
    option = gameData.randrange(0, 7)
    return option, pre[str(option)] + name + post[str(option)]


def seerWerewolf(option, name):
    pre = loc(lang, "seerWerewolfPre", option)
    post = loc(lang, "seerWerewolfPost", option)
    return pre + name + post


def seerNoWerewolf(option, name):
    pre = loc(lang, "seerNoWerewolfPre", option)
    post = loc(lang, "seerNoWerewolfPost", option)
    return pre + name + post
