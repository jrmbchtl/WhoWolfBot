"""Testing the join capability"""
from src.systemtest.systemtest import Systemtest


class JoinTest(Systemtest):
    """Test case for join function"""

    def get_name(self):
        return "JoinTest"

    def run(self):
        self.send_json({"commandType": "newGame",
                        "newGame": {"origin": 0, "seed": 42}, "fromId": 42})
        game_id = self.assert_any_message()["gameId"]
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 42, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        for player_id in range(1, 5):
            self.send_json(
                {"commandType": "join", "join": {"name": "Player " + str(player_id), "origin": 0},
                 "fromId": player_id, "gameId": game_id})
            self.assert_any_message()
        self.send_json({"commandType": "startGame", "fromId": 42, "gameId": game_id})
        for _ in range(8):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1},
                        "fromId": 4, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 3},
                        "fromId": 4, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1},
                        "fromId": 1, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
