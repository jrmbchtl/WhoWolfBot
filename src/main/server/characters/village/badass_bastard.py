"""module for the badass bastard"""
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType


class BadassBastard(VillagerTeam):
    """class for the badass bastard"""
    def __init__(self, alive=True):
        super().__init__(CharacterType.BADDASSBASTARD, "bbDescription", alive)
        self.second_live = True

    def has_second_live(self):
        return self.second_live

    def remove_second_live(self):
        """removes second live of role"""
        self.second_live = False
