from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc


class Witch(VillagerTeam):
    def __init__(self, alive=True):
        super(Witch, self).__init__(CharacterType.WITCH, "witchDescription", alive)
        self.hasLivePotion = True
        self.hasDeathPotion = True

    def wakeUp(self, gameData, playerId):
        if self.hasLivePotion and gameData.getWerewolfTarget() is not None:
            targetName = gameData.getPlayers()[gameData.getWerewolfTarget()].getName()
            text = targetName + (loc(gameData.getLang(), "witchSaveQuestion"))
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
                    playerId, witchDidSave(gameData, noSave, targetName)))
            elif choice == 1:
                gameData.sendJSON(Factory.createMessageEvent(
                    playerId, witchDidLetDie(gameData, noLetDie, targetName)))
            else:
                raise ValueError("The witch shouldn't have a choice " + choice + "!")
            gameData.dumpNextMessage(commandType="feedback")

        if self.hasDeathPotion:
            text = loc(gameData.getLang(), "witchKillQuestion")
            idToNo = {}
            indexToId = {}
            options = []
            index = 0
            for player in gameData.getAlivePlayerList():
                if player != playerId:
                    name = gameData.getAlivePlayers()[player].getName()
                    no, option = witchKill(gameData, name)
                    options.append(option)
                    idToNo[player] = no
                    indexToId[index] = player
                    index += 1

            no, option = witchKill(gameData, loc(gameData.getLang(), "Noone"))
            options.append(option)

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
                text = witchDidKill(gameData, idToNo[indexToId[choice]], targetName)
                gameData.sendJSON(Factory.createMessageEvent(playerId, text))
                gameData.dumpNextMessage(commandType="feedback")


def witchSave(gameData):
    dc = loc(gameData.getLang(), "witchSave")
    option = gameData.randrange(0, len(dc))
    return option, dc[str(option)]


def witchLetDie(gameData):
    dc = loc(gameData.getLang(), "witchLetDie")
    option = gameData.randrange(0, len(dc))
    return option, dc[str(option)]


def witchDidSave(gameData, option, name):
    pre = loc(gameData.getLang(), "witchDidSavePre", option)
    post = loc(gameData.getLang(), "witchDidSavePost", option)
    return pre + name + post


def witchDidLetDie(gameData, option, name):
    pre = loc(gameData.getLang(), "witchDidLetDiePre", option)
    post = loc(gameData.getLang(), "witchDidLetDiePost", option)
    return pre + name + post


def witchKill(gameData, name):
    pre = loc(gameData.getLang(), "witchKillPre")
    post = loc(gameData.getLang(), "witchKillPost")
    option = gameData.randrange(0, len(pre))
    return option, pre[str(option)] + name + post[str(option)]


def witchDidKill(gameData, option, name):
    pre = loc(gameData.getLang(), "witchDidKillPre", option)
    post = loc(gameData.getLang(), "witchDidKillPost", option)
    return pre + name + post
