"""module for the scallywag"""
from src.main.server import factory
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType
from src.main.server.factory import EditMode


class Scallywag(VillagerTeam):
    """class for the scallywag"""

    def __init__(self, alive=True):
        super().__init__(CharacterType.SCALLYWAG, "scallywagDescription", alive)
        self.second_live = True
        self.bomb_owner = None

    def wake_up(self, game_data, player_id):
        if self.bomb_owner is None:
            option, text = game_data.get_message("scallywagQuestion",
                                                 config={"rndm": True, "ret_opt": True})
            options = []
            for player in game_data.get_alive_players():
                options.append(game_data.get_alive_players()[player].get_name())
            game_data.send_json(factory.create_choice_field_event(player_id, text, options))
            message_id = game_data.get_next_message("feedback", player_id)["feedback"]["messageId"]

            choice = game_data.get_next_message("reply", player_id)["reply"]["choiceIndex"]
            target_id = game_data.get_alive_player_list()[choice]
            self.bomb_owner = target_id
            name = game_data.get_alive_players()[target_id].get_name()
            text += "\n\n" + game_data.get_message_pre_post("scallywagResponse", name, option)
            game_data.send_json(
                factory.create_message_event(player_id, text, message_id, {"mode": EditMode.EDIT}))
            game_data.dump_next_message("feedback", player_id)
        else:
            index = game_data.get_player_list().index(self.bomb_owner)
            while True:
                index += 1
                if index >= len(game_data.get_player_list()):
                    index = 0
                if game_data.get_player_list()[index] in game_data.get_alive_players():
                    self.bomb_owner = game_data.get_player_list()[index]
                    break

    def kill(self, game_data, player_id, death_message=None):
        super().kill(game_data, player_id, death_message)
        if self.bomb_owner in game_data.get_alive_player_list():
            target = game_data.get_alive_players()[self.bomb_owner].get_character()
            target.kill(game_data, self.bomb_owner)
