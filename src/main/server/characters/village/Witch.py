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
            noSave, optionSave = gameData.getMessage("witchSave", rndm=True, retOpt=True)
            noLetDie, optionLetDie = gameData.getMessage(
                "witchLetDie", rndm=True, retOpt=True)
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
                    playerId, gameData.getMessagePrePost(
                        "witchDidSave", targetName, option=noSave)))
            elif choice == 1:
                gameData.sendJSON(Factory.createMessageEvent(
                    playerId, gameData.getMessagePrePost(
                        "witchDidLetDie", targetName, option=noSave)))
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
                    no, option = gameData.getMessagePrePost(
                        "witchKill", name, rndm=True, retOpt=True)
                    options.append(option)
                    idToNo[player] = no
                    indexToId[index] = player
                    index += 1
            no, option = gameData.getMessagePrePost(
                "witchKill", loc(gameData.getLang(), "Noone"), rndm=True, retOpt=True)
            options.append(option)

            gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
            messageId = gameData.getNextMessage(commandType="feedback")["feedback"]["messageId"]

            choice = gameData.getNextMessage(commandType="reply")["reply"]["choiceIndex"]

            if choice == len(gameData.getAlivePlayerList()) - 1:
                gameData.setWitchTarget(None)
                targetName = loc(gameData.getLang(), "noone")
            else:
                self.hasDeathPotion = False
                gameData.setWitchTarget(indexToId[choice])
                targetName = gameData.getAlivePlayers()[indexToId[choice]].getName()
                no = idToNo[indexToId[choice]]
            text += "\n\n" + gameData.getMessagePrePost("witchDidKill", targetName, no)
            gameData.sendJSON(Factory.createMessageEvent(
                playerId, text, messageId, Factory.EditMode.EDIT))
            gameData.dumpNextMessage(commandType="feedback")
