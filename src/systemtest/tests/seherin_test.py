"""Module for testing the seer"""
from src.systemtest.systemtest import Systemtest


class SeherinTest(Systemtest):
    """Test case for the seer"""

    def get_name(self):
        return "SeherinTest"

    def run(self):
        game_id = self.init_game(5, 42, 1)

        self.assert_any_message()

        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 3, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()

        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 4, "gameId": game_id})
        self.assert_any_message()

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
