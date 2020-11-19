from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc

lang = "DE"


class Witch(VillagerTeam):
    def __init__(self, alive=True):
        super(Witch, self).__init__(CharacterType.WITCH, alive)
        self.hasLivePotion = True
        self.hasDeathPotion = True

    def getDescription(self, gameData):
        dc = loc(lang, "witchDescription")
        return dc[str(gameData.randrange(0, len(dc)))]

    def wakeUp(self, gameData, playerId):
        if self.hasLivePotion and gameData.getWerewolfTarget() is not None:
            targetName = gameData.getPlayers()[gameData.getWerewolfTarget()].getName()
            text = targetName + (loc(lang, "witchSaveQuestion"))
            noSave, optionSave = witchSave(gameData)
            noLetDie, optionLetDie = witchLetDie(gameData)
            gameData.sendJSON(Factory.createChoiceFieldEvent(
                playerId, text, [optionSave, optionLetDie]))
            messageId = gameData.getNextMessage(commandType="feedback")["feedback"]["messageId"]

            choice = gameData.getNextMessage(
                commandType="reply", fromId=playerId)["reply"]["choiceIndex"]
            gameData.sendJSON(Factory.createMessageEvent(
                playerId, text, messageId, Factory.EditMode.EDIT))
            gameData.dumpNextMessage(commandType="feedback")
            if choice == 0:
                gameData.setWerewolfTarget(None)
                self.hasLivePotion = False
                gameData.sendJSON(Factory.createMessageEvent(
                    playerId, witchDidSave(noSave, targetName)))
            elif choice == 1:
                gameData.sendJSON(Factory.createMessageEvent(
                    playerId, witchDidLetDie(noLetDie, targetName)))
            else:
                raise ValueError("The witch shouldn't have a choice " + choice + "!")
            gameData.dumpNextMessage(commandType="feedback")

        if self.hasDeathPotion:
            text = loc(lang, "witchKillQuestion")
            idToNo = {}
            indexToId = {}
            options = []
            index = 0
            for player in gameData.getAlivePlayerList():
                if player != playerId:
                    no, option = witchKill(gameData)
                    option = gameData.getAlivePlayers()[player].getName() + option
                    options.append(option)
                    idToNo[player] = no
                    indexToId[index] = player
                    index += 1

            no, option = witchKill(gameData)
            options.append(loc(lang, "Noone") + option)

            gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
            messageId = gameData.getNextMessage(commandType="feedback")["feedback"]["messageId"]

            choice = gameData.getNextMessage(commandType="reply")["reply"]["choiceIndex"]
            gameData.sendJSON(Factory.createMessageEvent(
                playerId, text, messageId, Factory.EditMode.EDIT))
            gameData.dumpNextMessage(commandType="feedback")

            if choice == len(gameData.getAlivePlayerList()) - 1:
                gameData.setWitchTarget(None)
            else:
                self.hasDeathPotion = False
                gameData.setWitchTarget(indexToId[choice])
                targetName = gameData.getAlivePlayers()[indexToId[choice]].getName()
                text = witchDidKill(idToNo[indexToId[choice]], targetName)
                gameData.sendJSON(Factory.createMessageEvent(playerId, text))
                gameData.dumpNextMessage(commandType="feedback")


def witchSave(gameData):
    dc = loc(lang, "witchSave")
    option = gameData.randrange(0, len(dc))
    return option, dc[str(option)]


def witchLetDie(gameData):
    dc = loc(lang, "witchLetDie")
    option = gameData.randrange(0, len(dc))
    return option, dc[str(option)]


def witchDidSave(option, name):
    pre = loc(lang, "witchDidSavePre", option)
    post = loc(lang, "witchDidSavePost", option)
    return pre + name + post


def witchDidLetDie(option, name):
    pre = loc(lang, "witchDidLetDiePre", option)
    post = loc(lang, "witchDidLetDiePost", option)
    return pre + name + post


def witchKill(gameData):
    dc = loc(lang, "witchKill")
    option = gameData.randrange(0, len(dc))
    return option, dc[str(option)]


def witchDidKill(option, name):
    pre = loc(lang, "witchDidKillPre", option)
    post = loc(lang, "witchDidKillPost", option)
    return pre + name + post
