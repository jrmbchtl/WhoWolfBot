"""module for the werewolf character"""
from src.main.server.characters.teams import WerewolfTeam
from src.main.server.characters.types import CharacterType


class Werewolf(WerewolfTeam):
    """class for a standard werewolf"""
    def __init__(self, alive=True):
        super().__init__(CharacterType.WEREWOLF, "werewolfDescription", alive)
