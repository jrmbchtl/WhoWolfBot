from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc


class Villager(VillagerTeam):
    def __init__(self, role=CharacterType.VILLAGER, alive=True):
        super(Villager, self).__init__(role, alive)

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "villagerDescription")
        return dc[str(gameData.randrange(0, len(dc)))]


class Villagerf(Villager):
    def __init__(self, alive=True):
        super(Villagerf, self).__init__(CharacterType.VILLAGERF, alive)

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "villagerfDescription")
        return dc[str(gameData.randrange(0, len(dc)))]
