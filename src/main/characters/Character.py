import random

from src.main import Factory


class Character(object):

    def __init__(self, team, role, isAlive=True):
        super(Character, self)
        self.isAlive = isAlive
        self.role = role
        self.team = team

    def isAlive(self):
        return self.isAlive

    def getTeam(self):
        return self.team

    def setTeam(self, team):
        self.team = team

    def getRole(self):
        return self.role

    def setRole(self, role):
        self.role = role

    def getDescription(self):
        pass

    def kill(self, gameData, playerId, dm=None):
        self.isAlive = False
        if dm is None:
            dm = gameData.getPlayers()[playerId].getName() + deathMessage()
        gameData.sendJSON(Factory.createMessageEvent(gameData.getOrigin(), deathMessage))
        gameData.dumpNextMessageDict()
        gameData.sendJSON(Factory.createMessageEvent(playerId, deathMessage))
        gameData.dumpNextMessageDict()

    def wakeUp(self, gameData, playerId):
        pass

    def initialWake(self, gameData, playerId):
        pass

    def getCharacterType(self):
        return self.role


def deathMessage():
    desc_no = random.randrange(1, 16)
    switcher = {
        1: " ist diese Nacht leider gestorben.",
        2: " erblickt das Licht des neuen Tages nicht mehr.",
        3: " wurde massakriert aufgefunden.",
        4: " existiert nur noch in Stücken.",
        5: " hat die letzten Stunden nicht überlebt.",
        6: " ist nicht mehr aufzufinden.",
        7: " war ein guter Kamerad.",
        8: " hat seinen letzten Kampf verloren.",
        9: " hat den Löffel abgegeben.",
        10: " besucht nun die ewigen Jagdgründe.",
        11: " hat leider ins Gras gebissen.",
        12: " wird nie wieder an den Freuden des Dorfes teilhaben.",
        13: " ist von uns gegangen.",
        14: " ist über die Wupper gegangen.",
        15: " hat das Zeitliche gesegnet."
    }
    return switcher[desc_no]
