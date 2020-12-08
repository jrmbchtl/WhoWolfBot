"""module for the berserk"""
from src.main.localization import get_localization as loc
from src.main.server import factory
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType


class Berserk(VillagerTeam):
    """class for the berserk"""

    def __init__(self, alive=True):
        super().__init__(CharacterType.BERSERK, "berserkDescription", alive)
        self.lives = 2

    def wake_up(self, game_data, player_id):
        if self.lives == 2:
            text = loc(game_data.get_lang(), "berserkTwoLives")
        else:
            text = loc(game_data.get_lang(), "berserkOneLive")
        option, question = game_data.get_message("berserkQuestion",
                                                 config={"rndm": True, "ret_opt": True})
        text += question
        options = []
        players = game_data.get_alive_players()
        for player in players:
            options.append(players[player].get_name())
        options.append(loc(game_data.get_lang(), "noone"))
        game_data.send_json(factory.create_choice_field_event(player_id, text, options))
        message_id = game_data.get_next_message("feedback", player_id)

        choice = game_data.get_next_message("reply", player_id)["reply"]["choiceIndex"]
        text += "\n\n" + game_data.get_message_pre_post(
            "berserkResponse", options[choice], option=option)
        game_data.send_json(factory.create_message_event(
            player_id, text, message_id, config={"mode": factory.EditMode.EDIT}))
        game_data.dump_next_message("feedback", player_id)

        if choice < len(players):
            self.lives -= 1
            game_data.set_nightly_target(game_data.get_alive_player_list()[choice],
                                         CharacterType.BERSERK)
            if self.lives <= 0:
                game_data.set_nightly_target(player_id, CharacterType.BERSERK)

    def werewolf_kill_attempt(self):
        self.lives -= 1
        return self.lives <= 0
