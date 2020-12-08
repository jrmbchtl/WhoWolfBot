"""module for the seer"""
from src.main.server import factory
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType
from src.main.server.characters.types import TeamType
from src.main.server.factory import EditMode


class Seer(VillagerTeam):
    """class for the seer"""
    def __init__(self, alive=True):
        super().__init__(CharacterType.SEER, "seerDescription", alive)

    def wake_up(self, game_data, player_id):
        options = []
        player_index_list = []
        player_to_option = {}
        for player in game_data.get_alive_players():
            if player != player_id:
                name = game_data.get_alive_players()[player].get_name()
                option, text = game_data.get_message_pre_post(
                    "seerOptions", name, config={"rndm": True, "ret_opt": True})
                options.append(text)
                player_to_option[player] = option
                player_index_list.append(player)
        text = game_data.get_message("seerQuestion", config={"rndm": True})
        game_data.send_json(factory.create_choice_field_event(player_id, text, options))
        message_id = game_data.get_next_message(
            command_type="feedback", from_id=player_id)["feedback"]["messageId"]

        choice = game_data.get_next_message(
            command_type="reply", from_id=player_id)["reply"]["choiceIndex"]

        game_data.send_json(
            factory.create_message_event(player_id, text, message_id, {"mode": EditMode.EDIT}))
        game_data.dump_next_message(command_type="feedback", from_id=player_id)

        name = game_data.get_alive_players()[player_index_list[choice]].get_name()
        if game_data.get_alive_players()[player_index_list[choice]].\
                get_character().get_team() == TeamType.WEREWOLF:
            reply_text = game_data.get_message_pre_post("seerWerewolf", name, option=choice)
        else:
            reply_text = game_data.get_message_pre_post("seerNoWerewolf", name, option=choice)
        game_data.send_json(factory.create_message_event(player_id, reply_text))
        game_data.dump_next_message(command_type="feedback", from_id=player_id)
