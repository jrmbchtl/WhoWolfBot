"""Testing the badass bastard role"""
from src.systemtest.systemtest import Systemtest


class BadassBastardTest(Systemtest):
    """Test case for the badass bastard"""

    def get_name(self):
        return "BadassBastardTest"

    def run(self):
        role_change = {"rem_list": ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Harter\xa0Bursche"]}
        game_id = self.init_game(number_of_players=4, admin=42, role_change=role_change)
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 3}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        for i in range(0, 3):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": i},
                            "fromId": i + 1, "gameId": game_id})
            self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        for i in range(0, 4):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                            "fromId": i + 1, "gameId": game_id})
            self.assert_any_message()
        self.snippet_1(game_id)
        self.assert_receive_dict({'eventType': 'message', 'message':
            {'text': 'Player 4 hat die letzten Stunden nicht überlebt.', 'messageId': 0},
            'mode': 'write', 'target': 0, 'highlight': True, 'gameId': game_id, 'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
