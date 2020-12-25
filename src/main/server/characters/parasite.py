"""module for the parasite"""
from src.main.server import factory
from src.main.server.characters.character import Character
from src.main.server.characters.types import CharacterType
from src.main.server.characters.types import TeamType


class Parasite(Character):
    """class for the parasite"""
    def __init__(self, alive=True):
        super().__init__(TeamType.PARASITE, CharacterType.PARASITE, "parasiteDescription", alive)
        self.host = None

    def kill(self, game_data, player_id, death_message=None):
        if self.host is None or self.host not in game_data.get_alive_players():
            super().kill(game_data, player_id, death_message)
        else:
            message = game_data.get_alive_players()[player_id].get_name()
            message += game_data.get_message("noDeathMessage", config={"rndm": True})
            game_data.send_json(factory.create_message_event(game_data.get_origin(), message))
            game_data.dump_next_message(command_type="feedback")

    def wake_up(self, game_data, player_id):
        text = game_data.get_message("parasiteQuestion", config={"rndm": True})
        options = []
        options_id = []
        for p_id in game_data.get_alive_players():
            if p_id == player_id:
                continue
            options.append(game_data.get_alive_players()[p_id].get_name())
            options_id.append(p_id)
        options.append(game_data.get_message("Noone"))

        game_data.send_json(factory.create_choice_field_event(player_id, text, options))
        message_id = game_data.get_next_message(
            command_type="feedback", from_id=player_id)["feedback"]["messageId"]

        choice = game_data.get_next_message("reply", player_id)["reply"]["choiceIndex"]
        text += "\n\n" + options[choice]
        game_data.send_json(factory.create_message_event(
            player_id, text, message_id, config={"mode": factory.EditMode.EDIT}))
        game_data.dump_next_message("feedback", player_id)

        if choice == len(options) - 1:
            game_data.set_nightly_target(self.host, CharacterType.PARASITE)
            game_data.get_alive_players()[self.host].get_character().set_parasite(None)
            self.host = None
        else:
            new_host = options_id[choice]
            if self.host != new_host:
                game_data.set_nightly_target(self.host, CharacterType.PARASITE)
                if self.host is not None:
                    game_data.get_alive_players()[self.host].get_character().set_parasite(None)
                game_data.get_alive_players()[new_host].get_character().set_parasite(player_id)
            self.host = new_host
