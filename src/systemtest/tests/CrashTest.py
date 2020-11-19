import os

from src.systemtest.Systemtest import Systemtest


class CrashTest(Systemtest):

    def getName(self):
        return "CrashTest"

    def run(self):
        gameId = 2
        if not os.path.isfile("games/" + str(gameId) + ".game"):
            print("did not found games/2.game, but " + str(os.listdir("./")))
            self.initGame(4, 42, 16384)
            self.assertReceiveDict({"eventType": "choiceField", "choiceField":
                {"text": "Mit wem lassen sich die hungrigen Werwolfsmäuler am besten stopfen?",
                 "options": ['Player 1 auf einen Mitternachtsimbiss treffen',
                             'Player 2 in die Lasagne mischen',
                             'Player 3 mit einer Torte verwechseln',
                             'Player 4 zu Gulasch verarbeiten',
                             'niemanden mit einer Torte verwechseln'], "messageId": 0},
                "mode": "write", "target": 2, "highlight": False, "gameId": 2})
        else:
            print("game 2 should be running")
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                              "fromId": 3, "gameId": gameId})

            self.assertReceiveDict({"eventType": "message", "message":
                {"text": ("Mit wem lassen sich die hungrigen Werwolfsmäuler am besten stopfen?\n\n"
                          "Player 3 schlägt vor Player 1 auf einen Mitternachtsimbiss zu treffen."
                          "\n\nDie Werwölfe haben beschlossen, Player 1 auf einen "
                          "Mitternachtsimbiss zu treffen."), "messageId": 22},
                "mode": "edit", "target": 2, "highlight": False, "gameId": gameId})

            self.sc.sendJSON({"commandType": "terminate", "fromId": 42,
                              "gameId": gameId})
            self.clearRecBuffer()
