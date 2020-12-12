"""module for testing the whie wolf"""
from src.systemtest.systemtest import Systemtest


class WhiteWolfTest(Systemtest):
    """test case for white wolf"""

    def get_name(self):
        return "WhiteWolfTest"

    def run(self):
        game_id = self.role_setup()
        self.send_json({"commandType": "startGame", "fromId": 42, "gameId": game_id})
        for _ in range(0, 11):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 5, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 3, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1},
                        "fromId": 3, "gameId": game_id})
        for _ in range(0, 4):
            self.assert_any_message()
        for i in range(2, 5):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": i - 2},
                            "fromId": i, "gameId": game_id})
            self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        for i in range(2, 7):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                            "fromId": i, "gameId": game_id})
            self.assert_any_message()
        for _ in range(0, 6):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 3},
                        "fromId": 5, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 3},
                        "fromId": 3, "gameId": game_id})
        for _ in range(0, 5):
            self.assert_any_message()
        for i in range(3, 6):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1},
                            "fromId": i, "gameId": game_id})
            self.assert_any_message()
        for _ in range(0, 5):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2},
                        "fromId": 3, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2},
                        "fromId": 5, "gameId": game_id})
        for _ in range(0, 4):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 3, "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': ('Es gibt keine Dorfbewohner und keine normalen Werwölfe mehr, die von den dem'
                     ' weißen Werwolf verspeißt werden können.'), 'messageId': 0}, 'mode': 'write',
                                  'target': 0, 'highlight': True, 'gameId': game_id, 'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()

    def role_setup(self):
        """setting up the roles"""
        self.send_json({"commandType": "newGame", "newGame": {"origin": 0, "seed": 0},
                        "fromId": 42})
        rec = self.assert_any_message()
        game_id = rec["gameId"]
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 42,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        rem_list = ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"]
        for role in rem_list:
            self.send_json({"commandType": "remove", "remove": {"role": role}, "fromId": 42,
                            "gameId": game_id})
            self.assert_any_message()
        self.send_json({"commandType": "add", "add": {"role": "Weißer\xa0Wolf"},
                        "fromId": 42, "gameId": game_id})
        self.assert_any_message()
        for i in range(1, 7):
            self.send_json({"commandType": "register", "register": {
                "name": "Player " + str(i)}, "fromId": i, "gameId": game_id})
            for _ in range(0, 3):
                self.assert_any_message()
        return game_id
