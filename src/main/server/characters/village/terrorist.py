"""module for the terrorist"""
from src.main.server import factory
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType
from src.main.server.factory import EditMode


class Terrorist(VillagerTeam):
    """class for the terrorist"""
    def __init__(self, alive=True):
        super().__init__(CharacterType.TERRORIST, "terroristDescription", alive)
        self.message_id = None
        self.index = None

    def remove_message(self, game_data, player_id):
        """removes the explode message from the terrorist"""
        if self.message_id is None:
            return
        game_data.send_json(
            factory.create_message_event(player_id, " ", message_id=self.message_id,
                                         config={"mode": EditMode.DELETE}))
        self.message_id = None

    def wake_up(self, game_data, player_id):
        text = game_data.get_message("terroristQuestion", config={"rndm": True})
        self.index, option = game_data.get_message(
            "terroristOption", config={"rndm": True, "ret_opt": True})

        game_data.send_json(factory.create_choice_field_event(player_id, text, [option]))
        rec = game_data.get_next_message(command_type="feedback", from_id=player_id)
        self.message_id = rec["feedback"]["messageId"]

    def kill(self, game_data, player_id, death_message=None):
        self.remove_message(game_data, player_id)
        super().kill(game_data, player_id, death_message)

    def explode(self, game_data, player_id):
        """explodes the terrorist"""
        if not self.is_alive():
            return
        text = game_data.get_message("terroristAnnounce", option=self.index)
        game_data.send_json(factory.create_message_event(game_data.get_origin(), text))
        self.kill(game_data, player_id)
        self.__kill_next(game_data, player_id, direction=1)
        self.__kill_next(game_data, player_id, direction=-1)

    @staticmethod
    def __kill_next(game_data, player_id, direction=1):
        """kills the next player in a direction (1-> right, 2-> left)"""
        player_list = list(game_data.get_players().keys())
        player = player_list[(player_list.index(player_id) + direction) % len(player_list)]
        while not game_data.get_players()[player].get_character().is_alive():
            if player == player_id:
                return
            player = player_list[(player_list.index(player) + direction) % len(player_list)]
        game_data.get_alive_players()[player].get_character().kill(game_data, player)
