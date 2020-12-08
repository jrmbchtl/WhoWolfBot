"""module for the hunter"""
from src.main.server import factory
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType


class Hunter(VillagerTeam):
    """class for hte hunter"""
    def __init__(self, alive=True):
        super().__init__(CharacterType.HUNTER, "hunterDescription", alive)

    def kill(self, game_data, player_id, death_message=None):
        super().kill(game_data, player_id, death_message)
        announcement = game_data.get_players()[player_id].get_name() + game_data.get_message(
            "hunterReveal", config={"rndm": True})
        game_data.send_json(factory.create_message_event(game_data.get_origin(), announcement))
        game_data.dump_next_message(command_type="feedback", from_id=game_data.get_origin())
        text = game_data.get_message("hunterQuestion", config={"rndm": True})
        options = []
        id_to_choice = {}
        id_list = []
        for player in game_data.get_alive_player_list():
            if player in game_data.get_nightly_target():
                continue
            choice, message = game_data.get_message_pre_post(
                "hunterOptions", game_data.id_to_name(player),
                config={"rndm": True, "ret_opt": True})
            id_list.append(player)
            id_to_choice[player] = choice
            options.append(message)

        game_data.send_json(factory.create_choice_field_event(player_id, text, options))
        message_id = game_data.get_next_message(
            command_type="feedback", from_id=player_id)["feedback"]["messageId"]

        rec = game_data.get_next_message(command_type="reply", from_id=player_id)
        game_data.send_json(factory.create_message_event(
            player_id, text, message_id, config={"mode": factory.EditMode.EDIT}))
        game_data.dump_next_message(command_type="feedback", from_id=player_id)

        target_id = id_list[rec["reply"]["choiceIndex"]]
        death_message = game_data.get_players()[target_id].get_name()
        death_message += game_data.get_message("hunterShot", option=id_to_choice[target_id])
        game_data.get_players()[target_id].get_character().kill(game_data, target_id, death_message)
