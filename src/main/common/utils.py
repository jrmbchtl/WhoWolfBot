"""common util module"""
import json
import os
import random

DEFAULT_LANG = "EN"


class Utils:
    """common util class"""

    def __init__(self, seed):
        super().__init__()
        self.seed = seed
        random.seed(seed)

    @staticmethod
    def randrange(start, stop, step=1):
        """randrange using seed"""
        return random.randrange(start, stop, step)

    @staticmethod
    def random():
        """random using seed"""
        return random.random()

    @staticmethod
    def shuffle(lis):
        """shuffle using seed"""
        random.shuffle(lis)

    @staticmethod
    def get_decision(dic):
        """calculates vote decision"""
        choice_to_amount = {}
        for key in dic:
            if dic[key] not in choice_to_amount:
                choice_to_amount[dic[key]] = 1
            else:
                choice_to_amount[dic[key]] += 1

        maximum = 0
        unique = True
        for key in choice_to_amount:
            if choice_to_amount[key] > maximum:
                maximum = choice_to_amount[key]
                unique = True
            elif choice_to_amount[key] == maximum:
                unique = False

        if not unique:
            return None

        for key in choice_to_amount:
            if choice_to_amount[key] == maximum:
                return key
        return None

    @staticmethod
    def unique_decision(dic):
        """checks if a decision is unique"""
        if Utils.get_decision(dic) is None:
            return False
        return True


def get_lang(player_id):
    """returns the language chosen by the player"""
    player_id = str(player_id)
    if not os.path.isfile("lang.json"):
        config = {}
        with open("lang.json", "w") as json_file:
            json.dump(config, json_file)
        return DEFAULT_LANG
    with open("lang.json", "r") as json_file:
        config = json.load(json_file)
        if player_id in config:
            return config[player_id]["lang"]
        return DEFAULT_LANG


def set_lang(player_id, lang):
    """sets the language for a player"""
    player_id = str(player_id)
    if not os.path.isfile("lang.json"):
        config = {player_id: {"lang": lang}}
        with open("lang.json", "w") as json_file:
            json.dump(config, json_file)
    else:
        with open("lang.json", "r") as json_file:
            config = json.load(json_file)
            print(config)
            if player_id in config:
                config[player_id]["lang"] = lang
            else:
                config[player_id] = {"lang": lang}
            print(config)
        with open("lang.json", "w") as json_file:
            json.dump(config, json_file)
