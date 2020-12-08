"""module for the terrorwolf character"""
from src.main.server import factory
from src.main.server.characters.teams import WerewolfTeam
from src.main.server.characters.types import CharacterType
from src.main.server.factory import EditMode


class Terrorwolf(WerewolfTeam):
    """Character Terrorwolf"""

    def __init__(self, alive=True):
        super().__init__(CharacterType.TERRORWOLF, "terrorwolfDescription", alive)

    def kill(self, game_data, player_id, death_message=None):
        super().kill(game_data, player_id)
        name = game_data.get_players()[player_id].get_name()
        text = name + game_data.get_message("terrorwolfReveal", config={"rndm": True})
        game_data.send_json(
            factory.create_message_event(game_data.get_origin(), text))
        game_data.dump_next_message(command_type="feedback", from_id=game_data.get_origin())

        options = []
        for player in game_data.get_alive_players():
            options.append(game_data.get_alive_players()[player].get_name())

        text = game_data.get_message("terrorwolfQuestion", config={"rndm": True})
        game_data.send_json(factory.create_choice_field_event(player_id, text, options))
        message_id = game_data.get_next_message("feedback", player_id)["feedback"]["messageId"]

        rec = game_data.get_next_message(command_type="reply", from_id=player_id)
        game_data.send_json(factory.create_message_event(
            player_id, text, message_id, config={"mode": EditMode.EDIT}))
        game_data.dump_next_message(command_type="feedback", from_id=player_id)

        target_id = game_data.get_alive_player_list()[rec["reply"]["choiceIndex"]]
        name = game_data.get_alive_players()[target_id].get_name()
        death_message = name + game_data.get_message("terrorwolfKill", config={"rndm": True})
        game_data.get_alive_players()[target_id].get_character().kill(game_data, target_id,
                                                                      death_message)
