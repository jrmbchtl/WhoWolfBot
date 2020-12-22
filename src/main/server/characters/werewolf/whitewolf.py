"""module for the white wolf character"""
from src.main.server import factory
from src.main.server.characters.teams import WhitewolfTeam
from src.main.server.characters.types import CharacterType
from src.main.server.characters.types import TeamType
from src.main.common.localization import get_localization as loc
from src.main.server.factory import EditMode


class Whitewolf(WhitewolfTeam):
    """class for the white wolf character"""
    def __init__(self, alive=True):
        super().__init__(CharacterType.WHITEWOLF, "whitewolfDescription", alive)
        self.dont_wake = False

    def wake_up(self, game_data, player_id):
        if self.dont_wake:
            self.dont_wake = False
            return
        self.dont_wake = True
        ww_list = []
        players = game_data.get_alive_players()
        for player in players:
            if players[player].get_character().get_team() == TeamType.WEREWOLF:
                ww_list.append(player)
        options = []
        if len(ww_list) == 0:
            return
        for werwolf in ww_list:
            player = game_data.get_alive_players()[werwolf]
            options.append(player.get_name())
        options.append(loc(game_data.get_lang(), "Noone"))
        text = game_data.get_message("whitewolfQuestion", config={"rndm": True})
        game_data.send_json(factory.create_choice_field_event(player_id, text, options))
        message_id = game_data.get_next_message("feedback", player_id)

        rec = game_data.get_next_message("reply", player_id)
        choice = rec["reply"]["choiceIndex"]
        target_name = loc(game_data.get_lang(), "Noone")
        if choice < len(ww_list):
            target_id = ww_list[choice]
            game_data.set_nightly_target(target_id, CharacterType.WHITEWOLF)
            target_name = game_data.get_alive_players()[target_id].get_name()
        text += "\n" + target_name
        game_data.send_json(
            factory.create_message_event(player_id, text, message_id, {"mode": EditMode.EDIT}))
        game_data.dump_next_message("feedback", player_id)
