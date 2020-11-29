from src.main.server import Factory
from src.main.server.characters.Character import Character
from src.main.server.characters.Types import CharacterType
from src.main.server.characters.Types import TeamType


class Wolfdog(Character):
    def __init__(self, alive=True):
        super(Wolfdog, self).__init__(None, CharacterType.WOLFDOG, "wolfdogDescription", alive)

    def wakeUp(self, gameData, playerId):
        if self.getTeam() is not None:
            return
        intro = gameData.getMessage("wolfdogQuestion", rndm=True)
        indexWerewolf, optionWerewolf = gameData.getMessage(
            "wolfdogChooseWerewolf", rndm=True, retOpt=True)
        indexVillage, optionVillage = gameData.getMessage(
            "wolfdogChooseVillage", rndm=True, retOpt=True)
        gameData.sendJSON(
            Factory.createChoiceFieldEvent(playerId, intro, [optionWerewolf, optionVillage]))
        messageId = gameData.getNextMessage(
            commandType="feedback", fromId=playerId)["feedback"]["messageId"]

        rec = gameData.getNextMessage(commandType="reply", fromId=playerId)
        if rec["reply"]["choiceIndex"] == 0:
            self.setTeam(TeamType.WEREWOLF)
            intro += "\n\n" + gameData.getMessage("wolfdogChoseWerewolf", indexWerewolf)
        elif rec["reply"]["choiceIndex"] == 1:
            self.setTeam(TeamType.VILLAGER)
            intro += "\n\n" + gameData.getMessage("wolfdogChoseVillage", indexVillage)
        else:
            raise ValueError("How can u choose option " + rec["reply"]["choiceIndex"])
        gameData.sendJSON(
            Factory.createMessageEvent(playerId, intro, messageId, Factory.EditMode.EDIT))
        gameData.dumpNextMessage(commandType="feedback", fromId=playerId)
