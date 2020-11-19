import random

from src.main.server import Factory
from src.main.localization import getLocalization as loc

lang = "DE"


class Character(object):

    def __init__(self, team, role, alive=True):
        super(Character, self)
        self.alive = alive
        self.role = role
        self.team = team

    def isAlive(self):
        return self.alive

    def getTeam(self):
        return self.team

    def setTeam(self, team):
        self.team = team

    def getRole(self):
        return self.role

    def setRole(self, role):
        self.role = role

    def getDescription(self, gameData):
        pass

    def kill(self, gameData, playerId, dm=None):
        self.alive = False
        if dm is None:
            dm = gameData.getPlayers()[playerId].getName() + deathMessage()
        gameData.sendJSON(Factory.createMessageEvent(gameData.getOrigin(), dm, highlight=True))
        gameData.dumpNextMessage(commandType="feedback")
        gameData.sendJSON(Factory.createMessageEvent(playerId, dm, highlight=True))
        gameData.dumpNextMessage(commandType="feedback")

    def wakeUp(self, gameData, playerId):
        pass

    def getCharacterType(self):
        return self.role


def deathMessage():
    dc = loc(lang, "deathMessage")
    return dc[str(random.randrange(0, len(dc)))]
