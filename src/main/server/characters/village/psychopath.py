"""module for the psychopath"""
from src.main.server import factory
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType
from src.main.server.factory import EditMode


class Psychopath(VillagerTeam):
    """class for the psychopath"""

    def __init__(self, alive=True):
        super().__init__(CharacterType.PSYCHOPATH, "psychopathDescription", alive)

    def wake_up(self, game_data, player_id):
        if len(game_data.get_nightly_target()) == 0:
            text = game_data.get_message("psychopathQuestion", config={"rndm": True})
            options = []
            id_to_choice = {}
            for player in game_data.get_alive_players():
                name = game_data.get_alive_players()[player].get_name()
                choice, message = game_data.get_message_pre_post(
                    "psychopathOption", name, config={"rndm": True, "ret_opt": True})
                options.append(message)
                id_to_choice[player] = choice

            game_data.send_json(factory.create_choice_field_event(player_id, text, options))
            message_id = game_data.get_next_message("feedback", player_id)["feedback"]["messageId"]

            choice = game_data.get_next_message("reply", player_id)["reply"]["choiceIndex"]
            target_id = game_data.get_alive_player_list()[choice]
            name = game_data.get_alive_players()[target_id].get_name()
            text += "\n\n" + game_data.get_message_pre_post(
                "psychopathResponse", name, option=id_to_choice[target_id])

            game_data.send_json(
                factory.create_message_event(player_id, text, message_id, {"mode": EditMode.EDIT}))
            game_data.dump_next_message("feedback", player_id)

            game_data.set_nightly_target(target_id, CharacterType.PSYCHOPATH)
