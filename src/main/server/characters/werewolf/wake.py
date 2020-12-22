"""module for waking werewolves"""
from src.main.common.localization import get_localization as loc
from src.main.server import factory
from src.main.server.characters.character import Character
from src.main.server.characters.types import CharacterType
from src.main.server.characters.types import TeamType
from src.main.server.factory import EditMode
from src.main.common.utils import Utils


def wake(game_data):
    """waking up all werewolves"""
    werewolf_list = []
    options = []
    option_index_list = []
    for player in game_data.get_alive_player_list():
        character: Character = game_data.get_alive_players()[player].get_character()
        if character.get_team() == TeamType.WEREWOLF or character.get_team() == TeamType.WHITEWOLF:
            werewolf_list.append(player)
        index, option = game_data.get_message_pre_post(
            "werewolfOptions", game_data.id_to_name(player), config={"rndm": True, "ret_opt": True})
        options.append(option)
        option_index_list.append(index)
    index, option = game_data.get_message_pre_post(
        "werewolfOptions", loc(game_data.get_lang(), "noone"),
        config={"rndm": True, "ret_opt": True})
    options.append(option)
    option_index_list.append(index)
    text = game_data.get_message("werewolfQuestion", config={"rndm": True})

    message_id_dict = {}  # werewolfId to MessageId
    for werewolf in werewolf_list:
        game_data.send_json(factory.create_choice_field_event(werewolf, text, options))
        message_id_dict[werewolf] = game_data.get_next_message(
            command_type="feedback", from_id=werewolf)["feedback"]["messageId"]

    new_text, vote_dict = get_decision(
        {"game_data": game_data, "werewolf_list": werewolf_list}, text, option_index_list, options,
        message_id_dict)

    publish_decision({"game_data": game_data, "werewolf_list": werewolf_list}, vote_dict,
                     option_index_list, new_text, message_id_dict)


def get_decision(data, text, option_index_list, options, message_id_dict):
    """returns the decision of the werewolves"""
    game_data = data["game_data"]
    werewolf_list = data["werewolf_list"]
    new_text = ""
    vote_dict = {}  # stores werewolf and which index he voted for
    while len(werewolf_list) > len(vote_dict) or not Utils.unique_decision(vote_dict):
        rec = game_data.get_next_message(command_type="reply")
        vote_dict[rec["fromId"]] = rec["reply"]["choiceIndex"]
        new_text = text + "\n\n"
        for key in vote_dict:
            if vote_dict[key] == len(game_data.get_alive_player_list()):
                target_name = loc(game_data.get_lang(), "noone")
            else:
                target_id = game_data.get_alive_player_list()[vote_dict[key]]
                target_name = game_data.get_alive_players()[target_id].get_name()
            new_text += game_data.id_to_name(key) + loc(
                game_data.get_lang(), "werewolfSuggest") + game_data.get_message_pre_post(
                    "werewolfResponse", target_name, option_index_list[vote_dict[key]]) + "\n"
        if len(werewolf_list) == len(vote_dict) and Utils.unique_decision(vote_dict):
            break
        for werewolf in werewolf_list:
            game_data.send_json(factory.create_choice_field_event(
                werewolf, new_text, options, message_id_dict[werewolf], {"mode": EditMode.EDIT}))
            game_data.dump_next_message(command_type="feedback")

    return new_text, vote_dict


def publish_decision(data, vote_dict, option_index_list, text, message_id_dict):
    """sends the werewolf decision to all werewolves and sets the nightly target"""
    game_data = data["game_data"]
    werewolf_list = data["werewolf_list"]
    decision_index = Utils.get_decision(vote_dict)

    if decision_index == len(game_data.get_alive_player_list()):
        target_name = "niemanden"
    else:
        target_id = game_data.get_alive_player_list()[decision_index]
        target_name = game_data.get_alive_players()[target_id].get_name()
        game_data.set_nightly_target(target_id, CharacterType.WEREWOLF)

    decision = loc(game_data.get_lang(), "werewolfDecision") + game_data.get_message_pre_post(
        "werewolfResponse", target_name, option_index_list[decision_index])
    text += "\n" + decision

    for werewolf in werewolf_list:
        game_data.send_json(factory.create_message_event(
            werewolf, text, message_id_dict[werewolf], config={"mode": factory.EditMode.EDIT}))
        game_data.dump_next_message(command_type="feedback")
