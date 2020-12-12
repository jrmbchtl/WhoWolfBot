"""module for the game server"""
import json
import os

import requests

from src.main.localization import get_localization as loc
from src.main.server import factory
from src.main.server.characters import teams
from src.main.server.characters.types import CharacterType
from src.main.server.characters.village.badass_bastard import BadassBastard
from src.main.server.characters.village.berserk import Berserk
from src.main.server.characters.village.cupid import Cupid
from src.main.server.characters.village.hunter import Hunter
from src.main.server.characters.village.psychopath import Psychopath
from src.main.server.characters.village.redhat import Redhat
from src.main.server.characters.village.scallywag import Scallywag
from src.main.server.characters.village.seer import Seer
from src.main.server.characters.village.villager import Villager
from src.main.server.characters.village.villager import Villagerf
from src.main.server.characters.village.witch import Witch
from src.main.server.characters.werewolf import wake
from src.main.server.characters.werewolf.terrorwolf import Terrorwolf
from src.main.server.characters.werewolf.werewolf import Werewolf
from src.main.server.characters.werewolf.whitewolf import Whitewolf
from src.main.server.characters.werewolf.wolfdog import Wolfdog
from src.main.server.factory import EditMode
from src.main.server.game_data import GameData
from src.main.server.player import Player
from src.main.server.utils import Utils


class Server:
    """server class for games"""

    def __init__(self, server_conn, dic, queues, game_id):
        super()
        game_queue = queues["game_queue"]
        delete_queue = queues["delete_queue"]
        dic["game_id"] = game_id

        self.game_data = GameData(server_conn=server_conn, game_queue=game_queue, dic=dic,
                                  delete_queue=delete_queue)
        self.accused_dict = {}
        self.enabled_roles = ["wolfdog", "terrorwolf", "seer", "witch", "hunter"]
        self.disabled_roles = ["badassbastard", "redhat", "whitewolf", "cupid", "berserk", "psycho",
                               "scallywag"]
        self.settings_message_id = None
        self.menu_message_id = None
        self.game_id = game_id

    def start(self):
        """main method with game loop"""
        self.set_language()
        self.register()
        self.roll_roles()
        while not self.check_game_over():
            self.night()
            if self.check_game_over():
                break
            if len(self.game_data.get_alive_players()) <= 3:
                self.accuse_all()
            else:
                self.accuse()
            self.vote()
        message_id = self.menu_message_id
        target = self.game_data.get_origin()
        self.game_data.send_json({"eventType": "message", "message": {"messageId": message_id},
                                  "target": target, "mode": "delete"})
        print("game " + str(self.game_id) + " is over")
        file = "games/" + str(self.game_id) + ".game"
        if os.path.isfile(file):
            os.remove(file)

    def set_language(self):
        """set the game language"""
        message = loc(self.game_data.get_lang(), "languageQuestion")
        dic = loc()
        options = []
        for lang in dic:
            options.append(lang)
        self.game_data.send_json(
            factory.create_choice_field_event(self.game_data.get_admin(), message,
                                              options))
        message_id = self.game_data.get_next_message(
            command_type="feedback", from_id=self.game_data.get_admin())["feedback"]["messageId"]
        choice = self.game_data.get_next_message(command_type="reply",
                                                 from_id=self.game_data.get_admin())
        self.game_data.set_lang(options[choice["reply"]["choiceIndex"]])
        self.game_data.send_json(factory.create_message_event(self.game_data.get_admin(), "",
                                                              message_id,
                                                              {"mode": factory.EditMode.DELETE}))
        self.game_data.dump_next_message(command_type="feedback",
                                         from_id=self.game_data.get_admin())

    def update_register_menu(self, disable=False):
        """send updated register-menu to client"""
        message = loc(self.game_data.get_lang(), "gameMenu")
        message += "Code: " + self.game_id + "\n\n"
        message += loc(self.game_data.get_lang(), "players") + ":\n"
        for player in self.game_data.get_players():
            message += self.game_data.get_players()[player].get_name() + "\n"
        if not disable:
            options = [loc(self.game_data.get_lang(), "join"),
                       loc(self.game_data.get_lang(), "start"),
                       loc(self.game_data.get_lang(), "cancel")]
        else:
            options = [loc(self.game_data.get_lang(), "cancel")]
        if self.menu_message_id is None:
            send_dict = factory.create_choice_field_event(self.game_data.get_origin(), message,
                                                          options)
        else:
            send_dict = factory.create_choice_field_event(
                self.game_data.get_origin(), message, options, self.menu_message_id,
                {"mode": factory.EditMode.EDIT})
        self.game_data.send_json(send_dict)

        rec = self.game_data.get_next_message(command_type="feedback")
        self.menu_message_id = rec["feedback"]["messageId"]

    def register(self):
        """lets register"""
        self.update_register_menu()
        self.send_settings()
        rec = self.game_data.get_next_message()
        while (rec["commandType"] != "startGame"
               or rec["fromId"] != self.game_data.get_admin()
               or len(self.game_data.get_players()) < 4):
            if rec["commandType"] == "register":
                self.__handle_register(rec)
            elif rec["commandType"] == "join":
                player = Player(rec["register"]["name"])
                self.game_data.get_players()[rec["fromId"]] = player
                self.game_data.add_origin(rec["fromId"])
                self.update_register_menu()
            elif rec["commandType"] == "add":
                role = rev_lookup(loc(self.game_data.get_lang(), "roles"), rec["add"]["role"])
                if role not in self.enabled_roles and role in self.disabled_roles:
                    self.enabled_roles.append(role)
                    self.disabled_roles.remove(role)
                    self.send_settings()
            elif rec["commandType"] == "remove":
                role = rev_lookup(loc(self.game_data.get_lang(), "roles"), rec["remove"]["role"])
                if role in self.enabled_roles and role not in self.disabled_roles:
                    self.enabled_roles.remove(role)
                    self.disabled_roles.append(role)
                    self.send_settings()
            rec = self.game_data.get_next_message()
        self.update_register_menu(True)
        self.game_data.send_json(
            factory.create_message_event(self.game_data.get_admin(),
                                         message_id=self.settings_message_id,
                                         config={"mode": factory.EditMode.DELETE}))
        self.game_data.dump_next_message(command_type="feedback")

    def __handle_register(self, rec):
        """handles a client register"""
        if rec["fromId"] not in self.game_data.get_players():
            self.game_data.send_json(
                factory.create_message_event(rec["fromId"],
                                             loc(self.game_data.get_lang(), "hello")))
            tmp = self.game_data.get_next_message(command_type="feedback")
            if tmp["feedback"]["success"] == 0:
                self.game_data.send_json(factory.create_message_event(
                    self.game_data.get_origin(),
                    rec["register"]["name"] + loc(self.game_data.get_lang(), "plsOpen")))
                self.game_data.dump_next_message(command_type="feedback")
            else:
                self.game_data.send_json(
                    factory.create_message_event(
                        rec["fromId"], "", tmp["feedback"]["messageId"],
                        {"mode": factory.EditMode.DELETE}))
                self.game_data.dump_next_message(command_type="feedback")
                player = Player(rec["register"]["name"])
                self.game_data.get_players()[rec["fromId"]] = player
        else:
            self.game_data.get_players().pop(rec["fromId"], None)
        self.update_register_menu()

    def send_settings(self):
        """sends settings to admin"""
        target = self.game_data.get_admin()
        text = loc(self.game_data.get_lang(), "roleConfig")
        roles = self.enabled_roles.copy()
        for i in self.disabled_roles:
            roles.append(i)
        roles.sort()
        options = []
        for i in roles:
            role = loc(self.game_data.get_lang(), "roles", i)
            if i in self.enabled_roles:
                pre = loc(self.game_data.get_lang(), "removePre")
                post = loc(self.game_data.get_lang(), "removePost")
                options.append(pre + role + post)
            if i in self.disabled_roles:
                pre = loc(self.game_data.get_lang(), "addPre")
                post = loc(self.game_data.get_lang(), "addPost")
                options.append(pre + role + post)
        if self.settings_message_id is None:
            message_id = 0
            mode = factory.EditMode.WRITE
        else:
            message_id = self.settings_message_id
            mode = factory.EditMode.EDIT

        self.game_data.send_json(
            factory.create_choice_field_event(target, text, options, message_id, {"mode": mode}))
        self.settings_message_id = \
            self.game_data.get_next_message(command_type="feedback")["feedback"]["messageId"]

    def roll_roles(self):
        """gives everyone a role"""
        player_list = self.game_data.get_player_list()
        Utils.shuffle(player_list)

        werewolf_role_list = self.__get_werewolf_role_list(len(player_list))
        village_role_list = self.__get_villager_role_list()

        unique = [CharacterType.HUNTER, CharacterType.SEER, CharacterType.WITCH,
                  CharacterType.WOLFDOG, CharacterType.TERRORWOLF, CharacterType.BADDASSBASTARD,
                  CharacterType.REDHAT, CharacterType.CUPID, CharacterType.BERSERK,
                  CharacterType.PSYCHOPATH, CharacterType.SCALLYWAG]

        group_mod = Utils.random() * 0.2 + 0.9
        werewolf_amount = int(round(len(player_list) * (1.0 / 3.5) * group_mod, 0))
        for index, player in enumerate(player_list):
            if index < werewolf_amount:
                role = werewolf_role_list[Utils.randrange(0, len(werewolf_role_list))]
                self.game_data.get_players()[player].set_character(role)
                if role.get_character_type() in unique:
                    remove_character_type_from_list(werewolf_role_list, role.get_character_type())
            else:
                role = village_role_list[Utils.randrange(0, len(village_role_list))]
                self.game_data.get_players()[player].set_character(role)
                if role.get_character_type() in unique:
                    remove_character_type_from_list(village_role_list, role.get_character_type())
                if role.get_character_type() == CharacterType.HUNTER:
                    if "redhat" in self.enabled_roles:
                        for _ in range(0, 28):
                            village_role_list.append(Redhat())
            self.game_data.send_json(
                factory.create_message_event(
                    player, self.game_data.get_players()[player].get_character().get_description(
                        self.game_data)))
            self.game_data.dump_next_message(command_type="feedback")

    def night(self):
        """its night"""
        self.game_data.send_json(factory.create_message_event(
            self.game_data.get_origin(), self.__nightfall()))
        self.game_data.dump_next_message(command_type="feedback")

        sorted_player_dict = self.game_data.get_alive_players_dict_sorted()
        wake_werewolf = False
        for player_id in sorted_player_dict:
            self.game_data.clear_queue()
            player = sorted_player_dict[player_id]
            if player.get_character().get_role().value < 0:
                player.get_character().wake_up(self.game_data, player_id)
            elif not wake_werewolf:
                wake_werewolf = True
                wake.wake(self.game_data)
                self.game_data.clear_queue()
                player.get_character().wake_up(self.game_data, player_id)
            else:
                player.get_character().wake_up(self.game_data, player_id)

        target_list = []
        for target in self.game_data.get_nightly_target():
            target_list.append(target)
            self.kill_target(target)
        for target in target_list:
            self.game_data.remove_nightly_target(target)

    def kill_target(self, target_id):
        """kill target from night"""
        if target_id in self.game_data.get_alive_players():
            target = self.game_data.get_alive_players()[target_id].get_character()
            target.kill(self.game_data, target_id)

    def accuse_all(self):
        """accuse everyone"""
        self.accused_dict = {}
        for player in self.game_data.get_alive_players():
            self.accused_dict[player] = player

    def accuse(self):
        """lets accuse"""
        self.accused_dict = {}
        id_to_choice = {}
        options = []
        for player in self.game_data.get_alive_players():
            name = self.game_data.get_alive_players()[player].get_name()
            choice, option = self.__accuse_options(name)
            options.append(option)
            id_to_choice[player] = choice
        text = self.__accuse_intro()
        self.game_data.send_json(factory.create_choice_field_event(
            self.game_data.get_origin(), text, options))
        message_id = self.game_data.get_next_message(command_type="feedback")["feedback"][
            "messageId"]

        new_text = ""
        while len(self.accused_dict) < 3:
            rec = self.game_data.get_next_message(command_type="reply")
            if rec["fromId"] not in self.game_data.get_alive_players():
                continue
            self.accused_dict[rec["fromId"]] = \
                self.game_data.get_alive_player_list()[rec["reply"]["choiceIndex"]]
            new_text = text + "\n\n"
            for entry in self.accused_dict:
                target = self.accused_dict[entry]
                new_text += self.game_data.id_to_name(entry)
                new_text += self.__accuse_text(id_to_choice[target],
                                               self.game_data.id_to_name(target))
                new_text += "\n"
            self.game_data.send_json(factory.create_choice_field_event(
                self.game_data.get_origin(), new_text, options, message_id,
                {"mode": EditMode.EDIT}))
            self.game_data.dump_next_message(command_type="feedback")

        self.game_data.send_json(factory.create_message_event(
            self.game_data.get_origin(), new_text, message_id, {"mode": factory.EditMode.EDIT}))
        self.game_data.dump_next_message(command_type="feedback")
        self.game_data.clear_queue()

    def __accuse_options(self, name):
        """options for accusing"""
        pre = loc(self.game_data.get_lang(), "accuseOptionsPre")
        post = loc(self.game_data.get_lang(), "accuseOptionsPost")
        choice = Utils.randrange(0, len(pre))
        return choice, pre[str(choice)] + name + post[str(choice)]

    def __accuse_intro(self):
        """accusing begin message"""
        dic = loc(self.game_data.get_lang(), "accuseIntro")
        return dic[str(Utils.randrange(0, len(dic)))]

    def __accuse_text(self, option, name):
        """message for accusing"""
        pre = loc(self.game_data.get_lang(), "accuseTextPre", option)
        post = loc(self.game_data.get_lang(), "accuseTextPost", option)
        return pre + name + post

    def vote(self):
        """voting time"""
        id_to_choice, vote_dict = self.get_vote_dict()
        if Utils.unique_decision(vote_dict):
            victim_id = Utils.get_decision(vote_dict)
            death_message = self.game_data.id_to_name(victim_id) + self.__vote_judgement(
                id_to_choice[victim_id])
            self.game_data.get_alive_players()[victim_id].get_character() \
                .kill(self.game_data, victim_id, death_message)
        else:
            text = self.__patt_revote()
            id_to_choice, vote_dict = self.get_vote_dict(text)
            if Utils.unique_decision(vote_dict):
                victim_id = Utils.get_decision(vote_dict)
                death_message = self.game_data.id_to_name(victim_id) + self.__vote_judgement(
                    id_to_choice[victim_id])
                self.game_data.get_alive_players()[victim_id].get_character() \
                    .kill(self.game_data, victim_id, death_message)
            else:
                text = self.__patt_no_kill()
                self.game_data.send_json(
                    factory.create_message_event(self.game_data.get_origin(), text))
                self.game_data.dump_next_message(command_type="feedback")

    def get_vote_dict(self, text=None):
        """gets who voted for who"""
        vote_dict = {}  # stores who voted for which index

        if text is None:
            text = self.__vote_intro()
        options = []
        id_to_choice = {}
        index_to_id = {}
        for index, p_id in enumerate(self.accused_dict):
            choice, option = self.__vote_options(self.game_data.id_to_name(self.accused_dict[p_id]))
            id_to_choice[self.accused_dict[p_id]] = choice
            options.append(option)
            index_to_id[index] = self.accused_dict[p_id]
        self.game_data.send_json(factory.create_choice_field_event(
            self.game_data.get_origin(), text, options))
        message_id = self.game_data.get_next_message(command_type="feedback")["feedback"][
            "messageId"]

        new_text = ""
        while len(vote_dict) < len(self.game_data.get_alive_players()):
            rec = self.game_data.get_next_message(command_type="reply")
            if rec["commandType"] == "reply":
                if rec["fromId"] not in self.game_data.get_alive_players():
                    continue
                vote_dict[rec["fromId"]] = rec["reply"]["choiceIndex"]
                new_text = text + "\n"
                for key in vote_dict:
                    target_id = index_to_id[vote_dict[key]]
                    new_text += "\n" + self.game_data.id_to_name(key)
                    new_text += self.__voted_for(id_to_choice[target_id],
                                                 self.game_data.id_to_name(target_id))

                self.game_data.send_json(factory.create_choice_field_event(
                    self.game_data.get_origin(), new_text, options, message_id,
                    config={"mode": factory.EditMode.EDIT}))
                self.game_data.dump_next_message(command_type="feedback")

        self.game_data.send_json(factory.create_message_event(
            self.game_data.get_origin(), new_text, message_id, {"mode": factory.EditMode.EDIT}))
        self.game_data.get_next_message(command_type="feedback")
        # change voteDict to store voterId -> votedId
        for p_id in vote_dict:
            vote_dict[p_id] = index_to_id[vote_dict[p_id]]
        self.game_data.clear_queue()
        return id_to_choice, vote_dict

    def __vote_intro(self):
        """message for vote introduction"""
        dic = loc(self.game_data.get_lang(), "voteIntro")
        return dic[str(Utils.randrange(0, len(dic)))]

    def __vote_options(self, name):
        """returns all vote options"""
        pre = loc(self.game_data.get_lang(), "voteOptionsPre")
        post = loc(self.game_data.get_lang(), "voteOptionsPost")
        choice = Utils.randrange(0, len(pre))
        return choice, pre[str(choice)] + name + post[str(choice)]

    def __voted_for(self, option, name):
        """message who voted for what"""
        pre = loc(self.game_data.get_lang(), "votedForPre", option)
        post = loc(self.game_data.get_lang(), "votedForPost", option)
        return pre + name + post

    def __vote_judgement(self, option):
        """message vor vote result"""
        return loc(self.game_data.get_lang(), "voteJudgement", option)

    def __patt_revote(self):
        """message for first draw"""
        dic = loc(self.game_data.get_lang(), "pattRevote")
        return dic[str(Utils.randrange(0, len(dic)))]

    def __patt_no_kill(self):
        """message for 2nd draw"""
        dic = loc(self.game_data.get_lang(), "pattNoKill")
        return dic[str(Utils.randrange(0, len(dic)))]

    def __nightfall(self):
        """message for nightfall"""
        dic = loc(self.game_data.get_lang(), "nightfall")
        return dic[str(Utils.randrange(0, len(dic)))]

    def check_game_over(self):
        """check if game is over"""
        if len(self.game_data.get_alive_players()) == 0:
            self.game_data.send_json(factory.create_message_event(
                self.game_data.get_origin(), self.__all_dead(), config={"highlight": True}))
            self.game_data.dump_next_message(command_type="feedback")
            return True
        if len(self.game_data.get_alive_players()) == 2:
            ids = self.game_data.get_alive_player_list()
            if self.game_data.get_alive_players()[ids[0]].get_character().get_beloved() == ids[1]:
                self.game_data.send_json(
                    factory.create_message_event(self.game_data.get_origin(), self.__love_win(),
                                                 config={"highlight": True}))
                self.game_data.dump_next_message()
                return True
        first_player_id = self.game_data.get_alive_player_list()[0]
        team = self.game_data.get_alive_players()[first_player_id].get_character().get_team()
        for player in self.game_data.get_alive_players():
            if self.game_data.get_alive_players()[player].get_character().get_team() == team:
                continue
            return False
        if team == teams.TeamType.WEREWOLF:
            self.game_data.send_json(
                factory.create_message_event(self.game_data.get_origin(), self.__werewolf_win(),
                                             config={"highlight": True}))
        elif team == teams.TeamType.WHITEWOLF:
            self.game_data.send_json(
                factory.create_message_event(self.game_data.get_origin(),
                                             self.__whitewolf_win(),
                                             config={"highlight": True}))
        else:
            self.game_data.send_json(
                factory.create_message_event(self.game_data.get_origin(), self.__village_win(),
                                             config={"highlight": True}))
        self.game_data.dump_next_message(command_type="feedback")
        return True

    def __all_dead(self):
        """everyone is dead"""
        dic = loc(self.game_data.get_lang(), "allDeadPre")
        choice = Utils.randrange(0, len(dic))
        if choice == 8:
            pre = dic[str(choice)]
            post = loc(self.game_data.get_lang(), "allDeadPost")
            msg = pre + str(json.loads(requests.get("http://api.open-notify.org/astros.json")
                                       .text)["number"]) + post
        else:
            msg = dic[str(choice)]
        return msg

    def __werewolf_win(self):
        """werewolves won"""
        dic = loc(self.game_data.get_lang(), "werewolfWin")
        choice = Utils.randrange(0, len(dic))
        return dic[str(choice)]

    def __whitewolf_win(self):
        """white wolf won"""
        dic = loc(self.game_data.get_lang(), "whitewolfWin")
        choice = Utils.randrange(0, len(dic))
        return dic[str(choice)]

    def __village_win(self):
        """villagers won"""
        dic = loc(self.game_data.get_lang(), "villageWin")
        choice = Utils.randrange(0, len(dic))
        return dic[str(choice)]

    def __love_win(self):
        """couple won"""
        dic = loc(self.game_data.get_lang(), "loveWin")
        choice = Utils.randrange(0, len(dic))
        return dic[str(choice)]

    def __get_werewolf_role_list(self, amount_of_players):
        """adding werewolves to tole list"""
        werewolf_role_list = []
        for _ in range(0, 40):
            werewolf_role_list.append(Werewolf())
        if amount_of_players >= 6 and "wolfdog" in self.enabled_roles:
            for _ in range(0, 40):
                werewolf_role_list.append(Wolfdog())
        if amount_of_players >= 6 and "whitewolf" in self.enabled_roles:
            for _ in range(0, 40):
                werewolf_role_list.append(Whitewolf())
        if "terrorwolf" in self.enabled_roles:
            for _ in range(0, 40):
                werewolf_role_list.append(Terrorwolf())
        return werewolf_role_list

    def __get_villager_role_list(self):
        """adding villagers to role list"""
        village_role_list = []
        for _ in range(0, 30):
            village_role_list.append(Villager())
            village_role_list.append(Villagerf())
        role_dict = {"hunter": Hunter, "seer": Seer, "witch": Witch, "badassbastard": BadassBastard,
                     "cupid": Cupid, "berserk": Berserk, "psycho": Psychopath,
                     "scallywag": Scallywag}
        for key in role_dict:
            if key in self.enabled_roles:
                for _ in range(0, 28):
                    village_role_list.append(role_dict[key]())
        return village_role_list


def remove_character_type_from_list(lis, character):
    """removes all characters from a list"""
    index = 0
    while index < len(lis):
        if lis[index].get_character_type() == character:
            del lis[index]
        else:
            index += 1


def rev_lookup(dic, value):
    """reverse lookup for dicts"""
    for key in dic:
        if dic[key] == value:
            return key
    return None
