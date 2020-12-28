"""module for testing the terrorist"""
from src.systemtest.systemtest import Systemtest


class TerroristTest(Systemtest):
    """general test case for the terrorist"""

    def init_terrorist(self):
        """initializes terrorist test"""
        role_change = {"rem_list": ["Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Terrorist"]}
        game_id = self.init_game(number_of_players=4, admin=42, role_change=role_change)
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 4},
                        "fromId": 3, "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField': {
            'text': 'Bereit?', 'options': ['Allahu Akbar'], 'messageId': 0}, 'mode': 'write',
                                  'target': 4, 'highlight': False, 'gameId': game_id, 'lang': 'DE'})
        self.assert_any_message()
        return game_id


class TerroristAccuseTest(TerroristTest):
    """test case for the terrorist exploding during accusations"""

    def get_name(self):
        return "TerroristAccuseTest"

    def run(self):
        game_id = self.init_terrorist()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 1, "gameId": game_id})
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1},
                        "fromId": 2, "gameId": game_id})
        self.assert_any_message()
        self.send_json({"commandType": "terrorist", "fromId": 4, "gameId": game_id})
        for _ in range(10):
            self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': ('Die Dorfbewohner veranstalten zur Feier des Tages einen Fest und stopfen den'
                     ' letzten Werwolf aus.'), 'messageId': 0}, 'mode': 'write', 'target': 0,
                                  'highlight': True, 'gameId': game_id, 'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()


class TerroristVoteTest(TerroristTest):
    """test case for the terrorist exploding during vote"""

    def get_name(self):
        return "TerroristVoteTest"

    def run(self):
        game_id = self.init_terrorist()
        for index in range(1, 4):
            self.send_json({"commandType": "reply", "reply": {
                "choiceIndex": index}, "fromId": index, "gameId": game_id})
            self.assert_any_message()
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 2,
                        "gameId": game_id})
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 1,
                        "gameId": game_id})
        self.assert_any_message()
        self.send_json({"commandType": "terrorist", "fromId": 4, "gameId": game_id})
        for _ in range(11):
            self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Das Dorf gewinnt.', 'messageId': 0}, 'mode': 'write', 'target': 0,
                                  'highlight': True, 'gameId': game_id, 'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
