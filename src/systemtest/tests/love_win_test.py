"""Testing the server when the loving couple wins"""
from src.systemtest.systemtest import Systemtest


class LoveWinTest(Systemtest):
    """Testcase for Couple Victory"""

    def get_name(self):
        return "LoveWinTest"

    def run(self):
        game_id = self.amor_couple_one_three()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 3,
                        "gameId": game_id})
        for _ in range(0, 4):
            self.assert_any_message()
        alive = [1, 3, 4]
        for i in alive:
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2}, "fromId": i,
                            "gameId": game_id})
            self.assert_any_message()
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message':
            {'text': 'Player 4 wurde gevierteilt.', 'messageId': 0},
            'mode': 'write', 'target': 0, 'highlight': True, 'gameId': game_id, 'lang': 'DE'})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message':
            {'text': 'Liebe überwindet alles.', 'messageId': 0}, 'mode': 'write',
            'target': 0, 'highlight': True, 'gameId': game_id, 'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
