"""module for testing the cupid"""
from src.systemtest.systemtest import Systemtest


class CupidTest(Systemtest):
    """test case for the cupid"""

    def get_name(self):
        return "CupidTest"

    def run(self):
        game_id = self.amor_couple_one_three()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Player 1 hat den Löffel abgegeben.',
            'messageId': 0}, 'mode': 'write', 'target': 0, 'highlight': True, 'gameId': game_id,
                                  'lang': 'DE'})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Player 3 hängt sich aus Trauer.', 'messageId': 0}, 'mode': 'write',
                                  'target': 0, 'highlight': True, 'gameId': game_id, 'lang': 'DE'})
        self.village_win_1(game_id)

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
