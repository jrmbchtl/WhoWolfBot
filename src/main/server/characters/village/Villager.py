from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType


class Villager(VillagerTeam):
    def __init__(self, alive=True):
        super(Villager, self).__init__(CharacterType.VILLAGER, "villagerDescription", alive)


class Villagerf(VillagerTeam):
    def __init__(self, alive=True):
        super(Villagerf, self).__init__(CharacterType.VILLAGERF, "villagerfDescription", alive)
