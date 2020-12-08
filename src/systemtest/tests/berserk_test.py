"""Testing the berserker"""
from src.systemtest.systemtest import Systemtest


class BerserkTest(Systemtest):
    """class to provide snippets for berserk tests"""

    def intro_one_life(self):
        """introduction with berserk having one life"""
        role_change = {"rem_list": ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Berserker"]}
        game_id = self.init_game(role_change=role_change)
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 3}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField':
            {'text': 'Du hast noch ein Leben.\n\nWen möchtest du ermorden?',
             'options': ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'niemanden'],
             'messageId': 0}, 'mode': 'write', 'target': 4, 'highlight': False, 'gameId': game_id,
            'lang': 'DE'})

        return game_id


class BerserkTest1(BerserkTest):
    """first test case for the berserk"""

    def get_name(self):
        return "BerserkTest1"

    def run(self):
        role_change = {"rem_list": ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Berserker"]}
        game_id = self.init_game(role_change=role_change)
        self.assert_any_message()
        self.snippet_2(game_id)
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField':
            {'text': 'Du hast noch 2 Leben.\n\nWen möchtest du ermorden?',
             'options': ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'niemanden'],
             'messageId': 0}, 'mode': 'write', 'target': 4, 'highlight': False, 'gameId': game_id,
            'lang': 'DE'})
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 4}, "fromId": 4,
                        "gameId": game_id})
        for _ in range(0, 4):
            self.assert_any_message()
        for i in range(2, 5):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": i,
                            "gameId": game_id})
            self.assert_any_message()
        self.snippet_1(game_id)
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField':
            {'text': 'Du hast noch 2 Leben.\n\nEs ist Zeit für dich, jemanden zu töten!',
             'options': ['Player 3', 'Player 4', 'niemanden'], 'messageId': 0}, 'mode': 'write',
            'target': 4, 'highlight': False, 'gameId': game_id, 'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()


class BerserkTest2(BerserkTest):
    """Second test case for the Berserker"""

    def get_name(self):
        return "BerserkTest2"

    def run(self):
        game_id = self.intro_one_life()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 4}, "fromId": 4,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        for i in range(1, 4):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": i}, "fromId": i,
                            "gameId": game_id})
            self.assert_any_message()
        self.snippet_3(game_id)
        for _ in range(0, 6):
            self.assert_any_message()
        self.snippet_2(game_id)
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField':
            {'text': ('Du hast noch ein Leben.\n\nDu erhälst die Möglichkeit, jemanden zu töten. '
                      'Wer wird es sein?'),
             'options': ['Player 1', 'Player 3', 'Player 4', 'niemanden'], 'messageId': 0},
            'mode': 'write', 'target': 4, 'highlight': False, 'gameId': game_id, 'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()


class BerserkTest3(BerserkTest):
    """Third test case for the berserk"""

    def get_name(self):
        return "BerserkTest3"

    def run(self):
        game_id = self.intro_one_life()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2}, "fromId": 4,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message':
            {'text': 'Player 3 hat den Löffel abgegeben.',
             'messageId': 0}, 'mode': 'write', 'target': 0, 'highlight': True, 'gameId': game_id,
            'lang': 'DE'})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message':
            {'text': 'Player 4 existiert nur noch in Stücken.', 'messageId': 0}, 'mode': 'write',
            'target': 0, 'highlight': True, 'gameId': game_id, 'lang': 'DE'})
        self.village_win_1(game_id)

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
