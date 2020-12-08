"""module for testing crash behaviour"""
import os

from src.systemtest.systemtest import Systemtest


class CrashTest(Systemtest):
    """test case simulating server crash"""

    def get_name(self):
        return "CrashTest"

    def run(self):
        game_id = 2
        if not os.path.isfile("games/" + str(game_id) + ".game"):
            self.init_game(4, 42, 16384)
            self.assert_receive_dict({"eventType": "choiceField", "choiceField":
                {"text": "Mit wem lassen sich die hungrigen Werwolfsmäuler am besten stopfen?",
                 "options": ['Player 1 auf einen Mitternachtsimbiss treffen',
                             'Player 2 in die Lasagne mischen',
                             'Player 3 mit einer Torte verwechseln',
                             'Player 4 zu Gulasch verarbeiten',
                             'niemanden mit einer Torte verwechseln'], "messageId": 0},
                "mode": "write", "target": 2, "highlight": False, "gameId": 2, 'lang': 'DE'})
        else:
            print("game 2 should be running")
            self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                            "fromId": 3, "gameId": game_id})

            self.assert_receive_dict({"eventType": "message", "message":
                {"text": ("Mit wem lassen sich die hungrigen Werwolfsmäuler am besten stopfen?\n\n"
                          "Player 3 schlägt vor Player 1 auf einen Mitternachtsimbiss zu treffen."
                          "\n\nDie Werwölfe haben beschlossen, Player 1 auf einen "
                          "Mitternachtsimbiss zu treffen."), "messageId": 24},
                "mode": "edit", "target": 2, "highlight": False, "gameId": game_id, 'lang': 'DE'})

            self.send_json({"commandType": "terminate", "fromId": 42,
                            "gameId": game_id})
            self.clear_rec_buffer()
