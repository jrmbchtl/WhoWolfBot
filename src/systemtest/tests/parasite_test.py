"""Testing the parasite role"""
from src.systemtest.systemtest import Systemtest


class ParasiteTest(Systemtest):
    """general class for testing the parasite"""

    def init_test(self):
        """initialize standard parasite test"""
        role_change = {"rem_list": ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Parasit"]}
        game_id = self.init_game(number_of_players=4, admin=42, role_change=role_change)
        self.assert_any_message()
        return game_id

    def finish_test(self, game_id):
        """finishing a standard parasite test"""
        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()


class ParasiteTryKillTest(ParasiteTest):
    """Test case for trying to kill the parasite"""

    def get_name(self):
        return "ParasiteTryKillTest"

    def run(self):
        game_id = self.init_test()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 3}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField': {
            'text': 'Wer soll heute Nacht dein Wirt werden?', 'options': [
                'Player 1', 'Player 2', 'Player 3', 'Niemanden'], 'messageId': 0}, 'mode': 'write',
                                  'target': 4, 'highlight': False, 'gameId': game_id, 'lang': 'DE'})
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 4,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        for index in range(1, 4):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": index},
                            "fromId": index, "gameId": game_id})
            self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        self.finish_test(game_id)


class HostKillTest(ParasiteTest):
    """Test case for killing the host of the parasite"""

    def get_name(self):
        return "HostKillTest"

    def run(self):
        game_id = self.init_test()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField': {
            'text': 'Wer soll heute Nacht dein Wirt werden?', 'options': [
                'Player 1', 'Player 2', 'Player 3', 'Niemanden'], 'messageId': 0}, 'mode': 'write',
                                  'target': 4, 'highlight': False, 'gameId': game_id, 'lang': 'DE'})
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 4,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Player 4 existiert nur noch in Stücken.', 'messageId': 0},
                                  'mode': 'write', 'target': 0, 'highlight': True,
                                  'gameId': game_id, 'lang': 'DE'})
        self.assert_any_message()
        self.assert_any_message()
        self.finish_test(game_id)


class ParasiteWinTest(ParasiteTest):
    """Test case letting the parasite win"""

    def get_name(self):
        return "ParasiteWinTest"

    def run(self):
        game_id = self.init_test()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField': {
            'text': 'Wer soll heute Nacht dein Wirt werden?', 'options': [
                'Player 1', 'Player 2', 'Player 3', 'Niemanden'], 'messageId': 0}, 'mode': 'write',
                                  'target': 4, 'highlight': False, 'gameId': game_id, 'lang': 'DE'})
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2}, "fromId": 4,
                        "gameId": game_id})
        for _ in range(4):
            self.assert_any_message()
        for index in range(2, 5):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": index,
                            "gameId": game_id})
            self.assert_any_message()
        for _ in range(5):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 4,
                        "gameId": game_id})
        for _ in range(3):
            self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Nur noch der Parasit lebt!', 'messageId': 0}, 'mode': 'write', 'target': 0,
                                  'highlight': True, 'gameId': game_id, 'lang': 'DE'})
        self.finish_test(game_id)
