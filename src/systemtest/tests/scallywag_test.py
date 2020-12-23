"""module for testing the scallywag"""
from src.systemtest.systemtest import Systemtest


class ScallywagTest(Systemtest):
    """test case for scallywag"""

    def get_name(self):
        return "ScallywagTest"

    def run(self):
        role_change = {"rem_list": ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Superschurke"]}
        game_id = self.init_game(role_change=role_change)
        self.snippet_4(game_id)
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField': {
            'text': 'Wem willst du die herzförmige Bombe geben?',
            'options': ['Player 1', 'Player 2', 'Player 3', 'Player 4'], 'messageId': 0},
                                  'mode': 'write', 'target': 4, 'highlight': False,
                                  'gameId': game_id, 'lang': 'DE'})
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 4,
                        "gameId": game_id})
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': ('Wem willst du die herzförmige Bombe geben?\n\n'
                     'Du hast Player 2 die Bombe gegeben.'),
            'messageId': 14}, 'mode': 'edit', 'target': 4, 'highlight': False, 'gameId': game_id,
                                  'lang': 'DE'})
        self.assert_any_message()
        for i in range(1, 4):
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": i}, "fromId": i,
                            "gameId": game_id})
            self.assert_any_message()
        self.assert_any_message()
        self.snippet_3(game_id)
        self.assert_any_message()
        for _ in range(0, 4):
            self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Player 4 hat die letzten Stunden nicht überlebt.', 'messageId': 0},
                                  'mode': 'write', 'target': 0, 'highlight': True,
                                  'gameId': game_id, 'lang': 'DE'})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Player 3 wurde massakriert aufgefunden.', 'messageId': 0}, 'mode': 'write',
                                  'target': 0, 'highlight': True, 'gameId': game_id, 'lang': 'DE'})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Es gibt keine Werwölfe mehr, die Dorfbewohner verspeißen wollen.',
            'messageId': 0}, 'mode': 'write', 'target': 0, 'highlight': True, 'gameId': game_id,
                                  'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
