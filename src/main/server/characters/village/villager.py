"""module for the villagers"""
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType


class Villager(VillagerTeam):
    """class for the male villagers"""
    def __init__(self, alive=True):
        super().__init__(CharacterType.VILLAGER, "villagerDescription", alive)


class Villagerf(VillagerTeam):
    """class for the female villagers"""
    def __init__(self, alive=True):
        super().__init__(CharacterType.VILLAGERF, "villagerfDescription", alive)
