from src.main.server import Factory
from src.main.server.GameData import GameData
from src.main.server.characters import Types
from src.main.server.characters.Character import Character
from src.main.localization import getLocalization as loc
from src.main.server.characters.Types import CharacterType


def wake(gameData: GameData):
    werewolfList = []
    options = []
    optionIndexList = []
    for player in gameData.getAlivePlayerList():
        c: Character = gameData.getAlivePlayers()[player].getCharacter()
        if c.getTeam() == Types.TeamType.WEREWOLF or c.getTeam() == Types.TeamType.WHITEWOLF:
            werewolfList.append(player)
        name = gameData.getAlivePlayers()[player].getName()
        index, option = gameData.getMessagePrePost("werewolfOptions", name, rndm=True, retOpt=True)
        options.append(option)
        optionIndexList.append(index)
    name = loc(gameData.getLang(), "noone")
    index, option = gameData.getMessagePrePost("werewolfOptions", name, rndm=True, retOpt=True)
    options.append(option)
    optionIndexList.append(index)
    text = gameData.getMessage("werewolfQuestion", rndm=True)

    messageIdDict = {}  # werewolfId to MessageId
    for werewolf in werewolfList:
        gameData.sendJSON(Factory.createChoiceFieldEvent(werewolf, text, options))
        messageIdDict[werewolf] = gameData.getNextMessage(
            commandType="feedback", fromId=werewolf)["feedback"]["messageId"]

    newText = ""
    voteDict = {}  # stores werewolf and which index he voted for
    while len(werewolfList) > len(voteDict) or not GameData.uniqueDecision(voteDict):
        rec = gameData.getNextMessage(commandType="reply")
        voteDict[rec["fromId"]] = rec["reply"]["choiceIndex"]
        newText = text + "\n\n"
        for key in voteDict:
            werewolfName = gameData.getAlivePlayers()[key].getName()
            if voteDict[key] == len(gameData.getAlivePlayerList()):
                targetName = loc(gameData.getLang(), "noone")
            else:
                targetId = gameData.getAlivePlayerList()[voteDict[key]]
                targetName = gameData.getAlivePlayers()[targetId].getName()
            newText += werewolfName + loc(
                gameData.getLang(), "werewolfSuggest") + gameData.getMessagePrePost(
                "werewolfResponse", targetName, optionIndexList[voteDict[key]]) + "\n"
        if len(werewolfList) == len(voteDict) and GameData.uniqueDecision(voteDict):
            break
        for werewolf in werewolfList:
            gameData.sendJSON(Factory.createChoiceFieldEvent(
                werewolf, newText, options, messageIdDict[werewolf], Factory.EditMode.EDIT))
            gameData.dumpNextMessage(commandType="feedback")

    publishDecision(gameData, werewolfList, voteDict, optionIndexList, newText, messageIdDict)


def publishDecision(gameData, werewolfList, voteDict, optionIndexList, text, messageIdDict):
    decisionIndex = GameData.getDecision(voteDict)

    if decisionIndex == len(gameData.getAlivePlayerList()):
        targetName = "niemanden"
    else:
        targetId = gameData.getAlivePlayerList()[decisionIndex]
        targetName = gameData.getAlivePlayers()[targetId].getName()
        gameData.setNightlyTarget(targetId, CharacterType.WEREWOLF)

    decision = loc(gameData.getLang(), "werewolfDecision") + gameData.getMessagePrePost(
        "werewolfResponse", targetName, optionIndexList[decisionIndex])
    text += "\n" + decision

    for werewolf in werewolfList:
        gameData.sendJSON(Factory.createMessageEvent(
            werewolf, text, messageIdDict[werewolf], Factory.EditMode.EDIT))
        gameData.dumpNextMessage(commandType="feedback")
