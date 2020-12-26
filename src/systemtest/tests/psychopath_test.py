"""Module for testing the psychopath"""
from src.systemtest.systemtest import Systemtest


class PsychopathTest(Systemtest):
    """Test case for the psychopath"""

    def get_name(self):
        return "PsychopathTest"

    def run(self):
        role_change = {"rem_list": ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Psychopath"]}
        game_id = self.init_game(role_change=role_change)
        self.snippet_4(game_id)
        self.assert_receive_dict({'eventType': 'choiceField', 'choiceField': {
            'text': 'Es ist bisher niemand gestorben. Das wird sich jetzt ändern...',
            'options': ['Player 1 mit einem Löffel erschlagen', 'Player 2 überfahren',
                        'Player 3 mit einem Löffel erschlagen',
                        'Player 4 ein Messer in die Brust rammen'], 'messageId': 0},
                                  'mode': 'write', 'target': 4, 'highlight': False,
                                  'gameId': game_id, 'lang': 'DE'})
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 4,
                        "gameId": game_id})
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': ('Es ist bisher niemand gestorben. Das wird sich jetzt ändern...\n\n'
                     'Du hast Player 1 mit einem Löffel erschlagen.'), 'messageId': 15},
                                  'mode': 'edit', 'target': 4, 'highlight': False,
                                  'gameId': game_id, 'lang': 'DE'})
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Player 1 existiert nur noch in Stücken.',
            'messageId': 0}, 'mode': 'write', 'target': 0, 'highlight': True, 'gameId': game_id,
                                  'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
