"""Testing the psychopath"""
from src.systemtest.systemtest import Systemtest


class PsychopathTest2(Systemtest):
    """Second Test case for the psychopath"""

    def get_name(self):
        return "PsychopathTest2"

    def run(self):
        role_change = {"rem_list": ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"],
                       "add_list": ["Psychopath"]}
        game_id = self.init_game(number_of_players=4, admin=42, role_change=role_change)

        self.assert_any_message()
        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 3,
                        "gameId": game_id})
        self.assert_any_message()
        self.assert_receive_dict({'eventType': 'message', 'message': {
            'text': 'Player 2 ist diese Nacht leider gestorben.', 'messageId': 0},
                                  'mode': 'write', 'target': 0, 'highlight': True,
                                  'gameId': game_id, 'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
