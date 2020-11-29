from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType


class Redhat(VillagerTeam):
    def __init__(self, alive=True):
        super(Redhat, self).__init__(CharacterType.REDHAT, "redhatDescription", alive)

    def canBeKilled(self, gameData):
        aliveP = gameData.getAlivePlayers()
        for p in aliveP:
            if aliveP[p].getCharacter().getRole() == CharacterType.HUNTER:
                return False
        return True
