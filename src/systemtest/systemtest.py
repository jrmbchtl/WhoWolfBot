"""Base module for all system tests"""
import time
from multiprocessing import Process

from src.main.common.server_connection import ServerConnection


class SystemtestBase:
    """Baseclass for all system tests"""

    def __init__(self, server_conn):
        super()
        self.__server_conn: ServerConnection = server_conn
        self.message_id = 1

    @staticmethod
    def get_name():
        """return the name of the test"""
        raise NameError("You should name your test!")

    def run(self):
        """runs the test"""

    def assert_receive_dict(self, dic):
        """assert that the next received message is equal to the one provided"""
        rec = self.__server_conn.receive_json()
        self.dict_compare(dic, rec)
        self.__verify_message(rec)

    def assert_any_message(self):
        """assert that the server gets any message"""
        rec = self.__server_conn.receive_json()
        self.__verify_message(rec)
        return rec

    def __verify_message(self, rec):
        """verifies to the server that a message was received"""
        game_id = rec["gameId"]
        from_id = rec["target"]
        orig_message_id = rec[rec["eventType"]]["messageId"]
        if rec["mode"] == "edit" or rec["mode"] == "delete":
            if isinstance(from_id, list):
                if isinstance(orig_message_id, list):
                    message_id = orig_message_id
                    for _ in range(len(from_id) - len(orig_message_id)):
                        message_id.append(self.message_id)
                        self.message_id += 1
                else:
                    message_id = [orig_message_id]
                    for _ in range(1, len(from_id)):
                        message_id.append(self.message_id)
                        self.message_id += 1
            else:
                message_id = orig_message_id
        else:
            if isinstance(from_id, list):
                message_id = []
                for _ in from_id:
                    message_id.append(self.message_id)
                    self.message_id += 1
            else:
                message_id = self.message_id
                self.message_id += 1
        self.__server_conn.send_json({"commandType": "feedback", "feedback": {
            "success": 1, "messageId": message_id}, "fromId": from_id, "gameId": game_id})

    def dict_compare(self, expected, actual):
        """compares two dicts"""
        for key in expected:
            assert_in(key, actual)
            if isinstance(expected[key], dict):
                self.dict_compare(expected[key], actual[key])
            else:
                assert_equal(expected[key], actual[key])
        for key in actual:
            assert_in(key, expected)
            if isinstance(actual[key], dict):
                self.dict_compare(expected[key], actual[key])
            else:
                assert_equal(expected[key], actual[key])

    def init_game(self, number_of_players=4, admin=42, seed=42, role_change=None):
        """handles everything including nightfall and returns the game_id"""
        if role_change is None:
            role_change = {"rem_list": [], "add_list": []}
        rem_list = role_change["rem_list"]
        add_list = role_change["add_list"]
        self.send_json({"commandType": "newGame", "newGame": {"origin": 0, "seed": seed},
                        "fromId": admin})
        rec = self.__server_conn.receive_json()
        game_id = rec["gameId"]
        self.__verify_message(rec)
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 42, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_receive_dict({"eventType": "choiceField", "choiceField": {
            "text": "Hier k\u00f6nnen Rollen hinzugef\u00fcgt oder entfernt werden",
            "options": ['Harter\xa0Bursche hinzufügen', 'Berserker hinzufügen', 'Amor hinzufügen',
                        'Jäger deaktivieren', 'Parasit hinzufügen', 'Psychopath hinzufügen',
                        'Rotkäppchen hinzufügen', 'Superschurke hinzufügen', 'Seherin deaktivieren',
                        'Terrorwolf deaktivieren', 'Weißer\xa0Wolf hinzufügen', 'Hexe deaktivieren',
                        'Wolfshund deaktivieren'],
            "messageId": 0}, "mode": "write", "target": 42, "highlight": False, "gameId": game_id,
                                  "lang": "DE"})
        for role in rem_list:
            self.send_json({"commandType": "remove", "remove": {"role": role}, "fromId": 42,
                            "gameId": game_id})
            self.assert_any_message()
        for role in add_list:
            self.send_json({"commandType": "add", "add": {"role": role},
                            "fromId": 42, "gameId": game_id})
            self.assert_any_message()
        for i in range(1, number_of_players + 1):
            self.send_json({"commandType": "register", "register": {
                "name": "Player " + str(i)}, "fromId": i, "gameId": game_id})
            for _ in range(0, 3):
                self.assert_any_message()
        self.send_json({"commandType": "startGame", "fromId": admin, "gameId": game_id})
        for _ in range(0, number_of_players + 3):
            self.assert_any_message()
        return game_id

    def clear_rec_buffer(self):
        """removes all mesaages from the queue"""
        proc = Process(target=clear_queue_helper, args=(self.__server_conn,))
        proc.start()
        time.sleep(1)
        proc.kill()

    def send_json(self, json):
        """sends a dictioniary to the server"""
        self.__server_conn.send_json(json)


class Systemtest(SystemtestBase):
    """class to prevent duplicate code"""

    def village_win_1(self, game_id):
        """assert that village wins scenario 1"""
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Mit dem Tod des letzten Werwolfes haben die Dorfbewohner jetzt ihre Ruhe.',
            'messageId': 0}, 'mode': 'write', 'target': 0, 'highlight': True, 'gameId': game_id,
                                  'lang': 'DE'})

    def amor_couple_one_three(self):
        """method to couple players 1 and 3"""
        role_change = {"rem_list": ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Amor"]}
        game_id = self.init_game(role_change=role_change)
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 4,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Du hast dich in Player 1 verliebt.', 'messageId': 0}, 'mode': 'write',
                                  'target': 3, 'highlight': False, 'gameId': game_id, 'lang': 'DE'})
        self.assert_any_message()

        return game_id

    def snippet_1(self, game_id):
        """random snippet 1"""
        for _ in range(0, 5):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()

    def snippet_2(self, game_id):
        """random snippet 2"""
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()

    def snippet_3(self, game_id):
        """random snippet 3"""
        self.assert_any_message()
        for i in range(1, 5):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": i,
                            "gameId": game_id})
            self.assert_any_message()

    def snippet_4(self, game_id):
        """random snippet 4"""
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 4}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()


def clear_queue_helper(server_conn):
    """helper for creating a clearing process"""
    while True:
        server_conn.receive_json()


def assert_equal(element1, element2):
    """assert equality between objects"""
    if not element1 == element2:
        raise AssertionError("\nExpected " + str(element1) + "\nBut got " + str(element2))


def assert_in(key, dic):
    """assert that the key is in the dictionary"""
    if key not in dic:
        raise AssertionError("\nkey " + str(key) + " not found in dict " + str(dic))
