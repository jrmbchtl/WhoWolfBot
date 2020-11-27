import random

from src.main.server import Factory
from src.main.localization import getLocalization as loc


class Character(object):

    def __init__(self, team, role, descString, alive=True):
        super(Character, self)
        self.alive = alive
        self.role = role
        self.team = team
        self.beloved = None
        self.descString = descString

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
        dc = loc(gameData.getLang(), self.descString)
        return dc[str(gameData.randrange(0, len(dc)))]

    def getBeloved(self):
        return self.beloved

    def setBeloved(self, beloved):
        self.beloved = beloved

    def werewolfKillAttempt(self):
        return True

    def hasSecondLive(self):
        return False

    def kill(self, gameData, playerId, dm=None):
        self.alive = False
        if dm is None:
            dm = gameData.getPlayers()[playerId].getName() + deathMessage(gameData)
        gameData.sendJSON(Factory.createMessageEvent(gameData.getOrigin(), dm, highlight=True))
        gameData.dumpNextMessage(commandType="feedback")
        gameData.sendJSON(Factory.createMessageEvent(playerId, dm, highlight=True))
        gameData.dumpNextMessage(commandType="feedback")
        if self.beloved is not None and self.beloved in gameData.getAlivePlayers():
            belovedName = gameData.getAlivePlayers()[self.beloved].getName()
            loveDm = belovedDm(gameData, belovedName)
            gameData.getAlivePlayers()[self.beloved].getCharacter()\
                .kill(gameData, self.beloved, loveDm)

    def wakeUp(self, gameData, playerId):
        pass

    def getCharacterType(self):
        return self.role

    def canBeKilled(self, gameData):
        return True


def deathMessage(gameData):
    dc = loc(gameData.getLang(), "deathMessage")
    return dc[str(random.randrange(0, len(dc)))]


def belovedDm(gameData, name):
    dc = loc(gameData.getLang(), "lovedOneKilled")
    return name + dc[str(random.randrange(0, len(dc)))]
