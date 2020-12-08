"""module for the different teams"""
from src.main.server.characters.character import Character
from src.main.server.characters.types import TeamType


class WerewolfTeam(Character):
    """team for all werewolfs"""

    def __init__(self, role, desc_string, alive):
        super().__init__(TeamType.WEREWOLF, role, desc_string, alive)


class VillagerTeam(Character):
    """team for the villagers"""

    def __init__(self, role, desc_string, alive):
        super().__init__(TeamType.VILLAGER, role, desc_string, alive)


class WhitewolfTeam(Character):
    """team for the white wolf"""

    def __init__(self, role, desc_string, alive):
        super().__init__(TeamType.WHITEWOLF, role, desc_string, alive)
