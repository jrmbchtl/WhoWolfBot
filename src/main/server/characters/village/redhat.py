"""module for the redhat"""
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType


class Redhat(VillagerTeam):
    """class for the redhat"""
    def __init__(self, alive=True):
        super().__init__(CharacterType.REDHAT, "redhatDescription", alive)

    def can_be_killed(self, game_data):
        alive_players = game_data.get_alive_players()
        for player_id in alive_players:
            if alive_players[player_id].get_character().get_role() == CharacterType.HUNTER:
                return False
        return True
