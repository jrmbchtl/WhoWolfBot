from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc


class Redhat(VillagerTeam):
    def __init__(self, alive=True):
        super(Redhat, self).__init__(CharacterType.REDHAT, alive)

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "redhatDescription")
        return dc[str(gameData.randrange(0, len(dc)))]

    def canBeKilled(self, gameData):
        aliveP = gameData.getAlivePlayers()
        for p in aliveP:
            if aliveP[p].getCharacter().getRole() == CharacterType.HUNTER:
                return False
        return True
