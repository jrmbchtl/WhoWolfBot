"""module for testing little red riding hood"""
from src.systemtest.systemtest import Systemtest


class RedhatTest(Systemtest):
    """test case for little red riding hood"""

    def get_name(self):
        return "RedhatTest"

    def run(self):
        role_change = {"rem_list": ["Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Rotkäppchen"]}
        game_id = self.init_game(number_of_players=4, admin=42, role_change=role_change)
        self.assert_any_message()
        self.snippet_2(game_id)
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField':
            {'text': ('Eine heiße Diskussion beginnt in Düsterwald. Vage Gerüchte werden auf '
                      'einmal zu harten Fakten, Werwölfe tarnen sich als normale Büger und '
                      'harmlose Dorfbewohner werden des brutalen Mordes beschuldigt.'), 'options':
                ['Player 1 anklagen', 'Player 2 anschuldigen', 'Player 3 bezichtigen',
                 'Player 4 beschuldigen'], 'messageId': 0}, 'mode': 'write', 'target': 0,
            'highlight': False, 'gameId': game_id, 'lang': 'DE'})
        for i in range(0, 3):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": i + 1},
                            "fromId": i + 1, "gameId": game_id})
            self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        for i in range(1, 5):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2}, "fromId": i,
                            "gameId": game_id})
            self.assert_any_message()
        for _ in range(0, 5):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 4,
                        "gameId": game_id})
        for _ in range(0, 5):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message':
            {'text': 'Player 1 erblickt das Licht des neuen Tages nicht mehr.', 'messageId': 0},
            'mode': 'write', 'target': 0, 'highlight': True, 'gameId': game_id, 'lang': 'DE'})
        self.assert_any_message()
        self.assert_any_message()

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
