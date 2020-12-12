"""module for handling the server data"""
import json
import os

from src.main.localization import get_localization as loc
from src.main.server.characters.types import CharacterType
from src.main.server.utils import Utils


class GameData:
    """stores data for each game"""

    def __init__(self, server_conn, dic, game_queue, delete_queue):
        super().__init__()

        self.dic = dic
        Utils(seed=self.__get_seed())
        self.players = {}
        self.conn = {"server_conn": server_conn, "game_queue": game_queue,
                     "delete_queue": delete_queue}
        self.lang = "EN"
        self.nightly_target = {}  # holds id -> from role
        self.rec_list = []
        self.number_sent = 0
        if "numberSent" in dic["newGame"] and "recList" in dic["newGame"]:
            self.rec_list = dic["newGame"]["recList"]
            self.number_sent = dic["newGame"]["numberSent"]

    def get_next_message(self, command_type=None, from_id=None):
        """returns next message fitting criteria from server connection"""
        data = None
        index = 0
        write_back = []
        while data is None:
            if index < len(self.rec_list):
                if (command_type is None or command_type == self.rec_list[index]["commandType"]) \
                        and (from_id is None or from_id == self.rec_list[index]["fromId"]):
                    data = self.rec_list.pop(index)
                else:
                    index += 1
            else:
                tmp = self.__get_game_queue().get()
                if (command_type is None or command_type == tmp["commandType"]) \
                        and (from_id is None or from_id == tmp["fromId"]):
                    data = tmp
                    self.__append_to_rec_list(data)
                else:
                    write_back.append(tmp)
        self.__add_to_delete_queue(data)
        for i in write_back:
            self.__get_game_queue().put(i)
        return data

    def dump_next_message(self, command_type=None, from_id=None):
        """dumps next message fitting criteria"""
        print("Dumped: " + str(self.get_next_message(command_type, from_id)))

    def clear_queue(self):
        """clears server connection"""
        while not self.__get_game_queue().empty():
            print("Cleared: " + str(self.__get_game_queue().get_nowait()))

    def __add_to_delete_queue(self, data):
        """remember to delete data later on"""
        if data["commandType"] != "feedback" or data["feedback"]["success"] == 0:
            return
        tmp = []
        while not self.__get_delete_queue().empty():
            item = self.__get_delete_queue().get()
            tmp.append(item)
        in_list = False
        for i in tmp:
            if i["messageId"] == data["feedback"]["messageId"] \
                    and i["target"] == data["fromId"]:
                in_list = True
            self.__get_delete_queue().put(i)
        if not in_list:
            self.__get_delete_queue().put({"target": data["fromId"],
                                           "messageId": data["feedback"]["messageId"]})

    def __append_to_rec_list(self, item):
        """remember data for restoration after crash"""
        self.__check_or_create()
        file_path = "games/" + str(self.__get_game_id()) + ".game"
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        data["recList"].append(item)
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)

    def __check_or_create(self):
        """check if game file exists, if not create it"""
        file_path = "games/" + str(self.__get_game_id()) + ".game"
        if not os.path.isfile(file_path):
            dic = {"seed": self.__get_seed(), "recList": [], "numberSent": 0,
                   "admin": self.get_admin(), "chatId": self.get_origin()}
            with open(file_path, "w") as json_file:
                json.dump(dic, json_file)

    def get_players(self):
        """returns all players in game"""
        return self.players

    def get_player_list(self):
        """returns list of all player ids"""
        lis = []
        for player in self.players:
            lis.append(player)
        return lis

    def get_alive_players(self):
        """returns all alive players"""
        alive_players = {}
        for player in self.players:
            if self.players[player].get_character().is_alive():
                alive_players[player] = self.players[player]
        return alive_players

    def get_alive_player_list(self):
        """returns all alive player id's"""
        player_list = []
        for player in self.get_alive_players():
            player_list.append(player)
        return player_list

    def get_alive_players_dict_sorted(self):
        """returns all alive players sorted by role number"""
        sorted_dict = {}
        while len(sorted_dict) < len(self.get_alive_players()):
            minimum = None
            for player in self.get_alive_players():
                if player in sorted_dict:
                    continue
                player_value = self.get_alive_players()[player].get_character().get_role().value
                if minimum is None:
                    minimum = player_value
                elif minimum > player_value:
                    minimum = player_value
            for player in self.get_alive_players():
                if self.get_alive_players()[player].get_character().get_role().value == minimum:
                    if player in sorted_dict:
                        continue
                    sorted_dict[player] = self.get_alive_players()[player]
                    break
        return sorted_dict

    def send_json(self, dic):
        """send json to clients"""
        if self.number_sent > 0:
            self.number_sent -= 1
        else:
            dic["gameId"] = self.__get_game_id()
            dic["lang"] = self.lang
            self.__get_server_conn().send_json(dic)
            self.__inc_number_sent()

    def __inc_number_sent(self):
        """increment number sent for restoration after crash"""
        self.__check_or_create()
        file_path = "games/" + str(self.__get_game_id()) + ".game"
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        data["numberSent"] += 1
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)

    def get_admin(self):
        """returns admin of game"""
        return self.dic["fromId"]

    def get_origin(self):
        """returns group chat of game"""
        return self.dic["newGame"]["origin"]

    def add_origin(self, client):
        """adds a client to the origin"""
        if isinstance(self.dic["newGame"]["origin"], list):
            self.dic["newGame"]["origin"].append(client)
        else:
            self.dic["newGame"]["origin"] = [self.dic["newGame"]["origin"], client]

    def __get_seed(self):
        """returns the seed of the game"""
        return self.dic["newGame"]["seed"]

    def __get_game_id(self):
        """returns the game_id of the game"""
        return self.dic["game_id"]

    def __get_server_conn(self):
        """returns the server connection"""
        return self.conn["server_conn"]

    def __get_game_queue(self):
        """returns the game queue"""
        return self.conn["game_queue"]

    def __get_delete_queue(self):
        """returns the delete queue"""
        return self.conn["delete_queue"]

    def set_nightly_target(self, target_id, from_role):
        """sets a target during the night"""
        if from_role == CharacterType.WEREWOLF:
            target = self.get_alive_players()[target_id].get_character()
            if target.has_second_live():  # badass bastard
                target.remove_second_live()
            elif not target.can_be_killed(self):  # redhat
                pass
            elif target.werewolf_kill_attempt():  # berserk
                self.nightly_target[target_id] = from_role
        else:
            self.nightly_target[target_id] = from_role

    def remove_nightly_target(self, target):
        """removes a nightly target by id"""
        self.nightly_target.pop(target, None)

    def get_nightly_target(self):
        """returns all nightly targets as dict"""
        return self.nightly_target

    def set_lang(self, lang):
        """sets the language"""
        self.lang = lang

    def get_lang(self):
        """returns the language"""
        return self.lang

    def id_to_name(self, player_id):
        """returns name of id"""
        return self.players[player_id].get_name()

    def get_message(self, key, option=None, config=None):
        """gets a message using localization"""
        if config is None:
            config = {}
        if "rndm" in config:
            rndm = config["rndm"]
        else:
            rndm = False
        if "ret_opt" in config:
            ret_opt = config["ret_opt"]
        else:
            ret_opt = False

        if option is None and not rndm:
            ret = loc(self.lang, key)
        elif option is not None:
            ret = loc(self.lang, key, option)
        else:
            dic = loc(self.lang, key)
            option = Utils.randrange(0, len(dic))
            ret = dic[str(option)]
        if ret_opt:
            return option, ret
        return ret

    def get_message_pre_post(self, key, name, option=None, config=None):
        """gets a message split into pre- and post a name"""
        if config is None:
            config = {}
        if "rndm" in config:
            rndm = config["rndm"]
        else:
            rndm = False
        if "ret_opt" in config:
            ret_opt = config["ret_opt"]
        else:
            ret_opt = False

        if option is None and not rndm:
            ret = loc(self.lang, key + "Pre")
            ret += name
            ret += loc(self.lang, key + "Post")
        elif option is not None:
            ret = loc(self.lang, key + "Pre", option)
            ret += name
            ret += loc(self.lang, key + "Post", option)
        else:
            dic = loc(self.lang, key + "Pre")
            option = Utils.randrange(0, len(dic))
            return self.get_message_pre_post(key, name, option, config)
        if ret_opt:
            return option, ret
        return ret
