"""module for the witch"""
from src.main.localization import get_localization as loc
from src.main.server import factory
from src.main.server.characters.teams import VillagerTeam
from src.main.server.characters.types import CharacterType


class Witch(VillagerTeam):
    """class for the witch"""

    def __init__(self, alive=True):
        super().__init__(CharacterType.WITCH, "witchDescription", alive)
        self.has_life_potion = True
        self.has_death_potion = True

    def wake_up(self, game_data, player_id):
        werewolf_target = None
        for i in game_data.get_nightly_target():
            if game_data.get_nightly_target()[i] == CharacterType.WEREWOLF:
                werewolf_target = i
                break
        if self.has_life_potion and werewolf_target is not None:
            self.handle_life_potion(game_data, player_id, werewolf_target)
        if self.has_death_potion:
            self.handle_death_potion(game_data, player_id)

    def handle_life_potion(self, game_data, player_id, werewolf_target):
        """handle the life potion of witch"""
        target_name = game_data.get_players()[werewolf_target].get_name()
        text = target_name + (loc(game_data.get_lang(), "witchSaveQuestion"))
        no_save, option_save = game_data.get_message("witchSave",
                                                     config={"rndm": True, "ret_opt": True})
        no_let_die, option_let_die = game_data.get_message(
            "witchLetDie", config={"rndm": True, "ret_opt": True})
        game_data.send_json(factory.create_choice_field_event(
            player_id, text, [option_save, option_let_die]))
        message_id = game_data.get_next_message(command_type="feedback")["feedback"][
            "messageId"]

        choice = game_data.get_next_message(
            command_type="reply", from_id=player_id)["reply"]["choiceIndex"]
        game_data.send_json(factory.create_message_event(
            player_id, text, message_id, config={"mode": factory.EditMode.EDIT}))
        game_data.dump_next_message(command_type="feedback")
        if choice == 0:
            game_data.remove_nightly_target(werewolf_target)
            self.has_life_potion = False
            game_data.send_json(factory.create_message_event(
                player_id, game_data.get_message_pre_post(
                    "witchDidSave", target_name, option=no_save)))
        elif choice == 1:
            game_data.send_json(factory.create_message_event(
                player_id, game_data.get_message_pre_post(
                    "witchDidLetDie", target_name, option=no_let_die)))
        else:
            raise ValueError("The witch shouldn't have a choice " + choice + "!")
        game_data.dump_next_message(command_type="feedback")

    def handle_death_potion(self, game_data, player_id):
        """handle witches death potion"""
        text = loc(game_data.get_lang(), "witchKillQuestion")
        id_to_no = {}
        index_to_id = {}
        options = []
        index = 0
        for player in game_data.get_alive_player_list():
            if player != player_id:
                name = game_data.get_alive_players()[player].get_name()
                number, option = game_data.get_message_pre_post(
                    "witchKill", name, config={"rndm": True, "ret_opt": True})
                options.append(option)
                id_to_no[player] = number
                index_to_id[index] = player
                index += 1
        number, option = game_data.get_message_pre_post(
            "witchKill", loc(game_data.get_lang(), "Noone"), config={"rndm": True, "ret_opt": True})
        options.append(option)

        game_data.send_json(factory.create_choice_field_event(player_id, text, options))
        message_id = game_data.get_next_message(command_type="feedback")["feedback"][
            "messageId"]

        choice = game_data.get_next_message(command_type="reply")["reply"]["choiceIndex"]

        if choice == len(game_data.get_alive_player_list()) - 1:
            target_name = loc(game_data.get_lang(), "noone")
        else:
            self.has_death_potion = False
            game_data.set_nightly_target(index_to_id[choice], CharacterType.WITCH)
            target_name = game_data.get_alive_players()[index_to_id[choice]].get_name()
            number = id_to_no[index_to_id[choice]]
        text += "\n\n" + game_data.get_message_pre_post("witchDidKill", target_name, number)
        game_data.send_json(factory.create_message_event(
            player_id, text, message_id, config={"mode": factory.EditMode.EDIT}))
        game_data.dump_next_message(command_type="feedback")
