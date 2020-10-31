from src.main.server import Factory
from src.main.server.GameData import GameData
from src.main.server.characters import Types
from src.main.server.characters.Character import Character


def wake(gameData: GameData):
    werwolfList = []
    options = []
    optionIndexList = []
    for player in gameData.getAlivePlayerList():
        c: Character = gameData.getAlivePlayers()[player].getCharacter()
        if c.getTeam() == Types.TeamType.WERWOLF:
            werwolfList.append(player)
        name = gameData.getAlivePlayers()[player].getName()
        index, option = werwolfOptions(gameData, name)
        options.append(option)
        optionIndexList.append(index)
    index, option = werwolfOptions(gameData, "niemanden")
    options.append(option)
    optionIndexList.append(index)
    text = werwolfChooseTarget(gameData)

    messageIdDict = {}  # werwolfId to MessageId
    for werwolf in werwolfList:
        gameData.sendJSON(Factory.createChoiceFieldEvent(werwolf, text, options))
        messageIdDict[werwolf] = gameData.getNextMessageDict()["feedback"]["messageId"]

    newText = ""
    voteDict = {}  # stores werwolf and which index he voted for
    while len(werwolfList) > len(voteDict) or not GameData.uniqueDecision(voteDict):

        rec = gameData.getNextMessageDict()
        if rec["commandType"] == "reply":
            voteDict[rec["reply"]["fromId"]] = rec["reply"]["choiceIndex"]
            newText = text + "\n\n"
            for key in voteDict:
                werwolfName = gameData.getAlivePlayers()[key].getName()
                if voteDict[key] == len(gameData.getAlivePlayerList()):
                    targetName = "niemanden"
                else:
                    targetId = gameData.getAlivePlayerList()[voteDict[key]]
                    targetName = gameData.getAlivePlayers()[targetId].getName()
                newText += werwolfName + " schlägt vor " + werwolfResponseOptions(
                    optionIndexList[voteDict[key]], targetName) + "\n"
            if len(werwolfList) == len(voteDict) and GameData.uniqueDecision(voteDict):
                break
            for werwolf in werwolfList:
                gameData.sendJSON(Factory.createChoiceFieldEvent(
                    werwolf, newText, options, messageIdDict[werwolf], Factory.EditMode.EDIT))
                gameData.dumpNextMessageDict()

    print("publishing werwolf decision")
    publishDecision(gameData, werwolfList, voteDict, optionIndexList, newText, messageIdDict)
    print("finished waking werwolfs")


def publishDecision(gameData, werwolfList, voteDict, optionIndexList, text, messageIdDict):
    decisionIndex = GameData.getDecision(voteDict)

    if decisionIndex == len(gameData.getAlivePlayerList()):
        targetName = "niemanden"
        gameData.setWerwolfTarget(None)
    else:
        targetId = gameData.getAlivePlayerList()[decisionIndex]
        targetName = gameData.getAlivePlayers()[targetId].getName()
        gameData.setWerwolfTarget(targetId)

    decision = "Die Werwölfe haben beschlossen, " \
               + werwolfResponseOptions(optionIndexList[decisionIndex], targetName)
    text += "\n" + decision

    for werwolf in werwolfList:
        gameData.sendJSON(Factory.createMessageEvent(
            werwolf, text, messageIdDict[werwolf], Factory.EditMode.EDIT))
        gameData.dumpNextMessageDict()


def werwolfChooseTarget(gameData):
    switcher = {
        0: "Die Werwölfe suchen ihr Opfer aus.",
        1: "Das Werwolfsrudel streift hungrig durch das Dorf, auf der Suche nach einem Imbiss.",
        2: ("Die Werwölfe erinnern sich an einen weisen Spruch: 'Wählt weise, denn jede Mahlzeit "
            "könnte eure letzte sein'."),
        3: "Auf der Suche nach Essen durchsuchen die Werwölfe das Dorf.",
        4: "Es ist Nacht. Es ist Mitternacht. Es ist Essenzeit!",
        5: "Zu Tische, Werwölfe!",
        6: "Auf wen die Werwölfe heute Nacht wohl Appetit haben?",
        7: "Werwölfe, sucht euer Opfer aus!",
        8: "Mit wem lassen sich die hungrigen Werwolfsmäuler am besten stopfen?",
        9: "Die Werwolfsmägen knurren vor Hunger - Zeit, sich etwas zu Essen zu suchen!",
        10: "Frischer Mensch - kommt auf den Tisch - so saftig süüüüüüüüüüüüüüüß!"
    }
    return switcher[gameData.randrange(0, 11)]


def werwolfOptions(gameData, name):
    switcher = {
        0: name + " reißen",
        1: name + " zu Gulasch verarbeiten",
        2: name + " als Geschnetzeltes genießen",
        3: name + " durch den Fleischwolf jagen",
        4: name + " den Hals umdrehen",
        5: name + " versnacken",
        6: name + " zur Stillung der Blutlust verwenden",
        7: name + " auf einen Mitternachtsimbiss treffen",
        8: name + " die Reißzähne in den Hals rammen",
        9: name + " zu Salami verarbeiten",
        10: name + " in die Lasagne mischen",
        11: name + " mit einer Torte verwechseln"
    }
    choice = gameData.randrange(0, 12)
    return choice, switcher[choice]


def werwolfResponseOptions(option, name):
    switcher = {
        0: name + " zu reißen.",
        1: name + " zu Gulasch zu verarbeiten.",
        2: name + " als Geschnetzeltes zu genießen.",
        3: name + " durch den Fleischwolf zu jagen.",
        4: name + " den Hals umzudrehen.",
        5: name + " zu versnacken.",
        6: name + " zur Stillung der Blutlust zu verwenden.",
        7: name + " auf einen Mitternachtsimbiss zu treffen.",
        8: name + " die Reißzähne in den Hals zu rammen.",
        9: name + " zu Salami zu verarbeiten.",
        10: name + " in die Lasagne zu mischen.",
        11: name + " mit einer Torte zu verwechseln."
    }
    return switcher[option]
