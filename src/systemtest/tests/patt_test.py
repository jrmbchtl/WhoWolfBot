"""Testing the server by creating draws"""
from src.systemtest.systemtest import Systemtest


class DrawTest(Systemtest):
    """abstract class for draw tests"""

    def setup_draw(self):
        """prepares draw"""
        game_id = self.init_game(number_of_players=4, admin=42)

        self.assert_any_message()

        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 3, "gameId": game_id})

        for i in range(0, 2):
            self.assert_any_message()

        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 4, "gameId": game_id})

        for i in range(0, 3):
            self.assert_any_message()

        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 3},
                        "fromId": 4, "gameId": game_id})

        for i in range(0, 2):
            self.assert_any_message()

        for i in range(1, 4):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": i},
                            "fromId": i, "gameId": game_id})
            self.assert_any_message()

        self.assert_any_message()
        self.assert_any_message()

        for i in range(0, 2):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                            "fromId": i + 1, "gameId": game_id})
            self.assert_any_message()

        for i in range(2, 4):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1},
                            "fromId": i + 1, "gameId": game_id})
            self.assert_any_message()

        self.assert_any_message()
        self.assert_any_message()
        return game_id


class PattTest(DrawTest):
    """Testcase for draw"""

    def get_name(self):
        return "PattTest"

    def run(self):
        game_id = self.setup_draw()

        for i in range(0, 4):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                            "fromId": i + 1, "gameId": game_id})
            self.assert_any_message()

        self.assert_receive_dict({'eventType': 'message', 'message':
            {'text': ('Es kann nur eine Person hingerichtet werden, irgendjemand sollte seine '
                      'Meinung ändern!\n\nPlayer 1 will Player 2 auf dem Scheiterhaufen sehen!\n'
                      'Player 2 will Player 2 auf dem Scheiterhaufen sehen!\nPlayer 3 will Player '
                      '2 auf dem Scheiterhaufen sehen!\nPlayer 4 will Player 2 auf dem '
                      'Scheiterhaufen sehen!'), 'messageId': 42}, 'mode': 'edit', 'target': 0,
            'highlight': False, 'gameId': game_id, 'lang': 'DE'})
        self.assert_any_message()

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()


class DoublePattTest(DrawTest):
    """Testcase for two draws"""

    def get_name(self):
        return "DoublePattTest"

    def run(self):
        game_id = self.setup_draw()

        for i in range(0, 2):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                            "fromId": i + 1, "gameId": game_id})
            self.assert_any_message()

        for i in range(2, 4):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1},
                            "fromId": i + 1, "gameId": game_id})
            self.assert_any_message()

        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message':
            {'text': 'Die Demokratie ist überfordert und beschließt, niemanden hinzurichten.',
             'messageId': 0}, 'mode': 'write', 'target': 0, 'highlight': False, 'gameId': game_id,
            'lang': 'DE'})

        self.assert_receive_dict({"eventType": "message", "message":
            {"text": ("Nach einem anstrengenden Tag hoffen viele Dorfbewohner nun auf eine "
                      "erholsame Nacht. Doch diese Nacht werden nicht alle gut schlafen..."),
             "messageId": 0}, "mode": "write", "target": 0, "highlight": False, "gameId": game_id,
            'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
