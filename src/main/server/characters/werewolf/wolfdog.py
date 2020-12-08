"""module for the wolf dog"""
from src.main.server import factory

from src.main.server.characters.character import Character
from src.main.server.characters.types import CharacterType
from src.main.server.characters.types import TeamType
from src.main.server.factory import EditMode


class Wolfdog(Character):
    """class for the wolf dog character"""
    def __init__(self, alive=True):
        super().__init__(None, CharacterType.WOLFDOG, "wolfdogDescription", alive)

    def wake_up(self, game_data, player_id):
        if self.get_team() is not None:
            return
        intro = game_data.get_message("wolfdogQuestion", config={"rndm": True})
        index_werewolf, option_werewolf = game_data.get_message(
            "wolfdogChooseWerewolf", config={"rndm": True, "ret_opt": True})
        index_village, option_village = game_data.get_message(
            "wolfdogChooseVillage", config={"rndm": True, "ret_opt": True})
        game_data.send_json(
            factory.create_choice_field_event(player_id, intro, [option_werewolf, option_village]))
        message_id = game_data.get_next_message(
            command_type="feedback", from_id=player_id)["feedback"]["messageId"]

        rec = game_data.get_next_message(command_type="reply", from_id=player_id)
        if rec["reply"]["choiceIndex"] == 0:
            self.set_team(TeamType.WEREWOLF)
            intro += "\n\n" + game_data.get_message("wolfdogChoseWerewolf", index_werewolf)
        elif rec["reply"]["choiceIndex"] == 1:
            self.set_team(TeamType.VILLAGER)
            intro += "\n\n" + game_data.get_message("wolfdogChoseVillage", index_village)
        else:
            raise ValueError("How can u choose option " + rec["reply"]["choiceIndex"])
        game_data.send_json(
            factory.create_message_event(player_id, intro, message_id, {"mode": EditMode.EDIT}))
        game_data.dump_next_message(command_type="feedback", from_id=player_id)
