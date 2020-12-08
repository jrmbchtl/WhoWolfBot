"""module for the cupid"""
from src.main.localization import get_localization as loc
from src.main.server import factory
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType


class Cupid(VillagerTeam):
    """class for the cupid"""

    def __init__(self, alive=True):
        super().__init__(CharacterType.CUPID, "cupidDescription", alive)
        self.was_waked = False

    def wake_up(self, game_data, player_id):
        if self.was_waked:
            return
        self.was_waked = True
        text = game_data.get_message("cupidQuestion", config={"rndm": True})
        options = []
        option_id = []
        player_list = game_data.get_alive_player_list()
        players = game_data.get_alive_players()
        for outer in range(0, len(players)):
            outer_player = player_list[outer]
            for inner in range(outer + 1, len(players)):
                inner_player = player_list[inner]
                options.append(players[outer_player].get_name() + " "
                               + loc(game_data.get_lang(), "and") + " "
                               + players[inner_player].get_name())
                option_id.append([outer_player, inner_player])
        game_data.send_json(factory.create_choice_field_event(player_id, text, options))
        message_id = game_data.get_next_message("feedback", player_id)

        choice = game_data.get_next_message("reply", player_id)["reply"]["choiceIndex"]
        text += "\n\n" + options[choice]
        game_data.send_json(factory.create_message_event(
            player_id, text, message_id, {"mode": factory.EditMode.EDIT}))
        game_data.dump_next_message("feedback", player_id)

        for outer in option_id[choice]:
            if option_id[choice][0] == outer:
                beloved_name = players[option_id[choice][1]].get_name()
                players[option_id[choice][0]].get_character().set_beloved(option_id[choice][1])
            else:
                beloved_name = players[option_id[choice][0]].get_name()
                players[option_id[choice][1]].get_character().set_beloved(option_id[choice][0])
            text = game_data.get_message_pre_post("fellInLove", beloved_name)
            game_data.send_json(factory.create_message_event(outer, text))
            game_data.dump_next_message("feedback", outer)
