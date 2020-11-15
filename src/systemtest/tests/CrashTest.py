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
                {"text": "Die Werw\u00f6lfe suchen ihr Opfer aus.", "options":
                    ["Player 1 in die Lasagne mischen", "Player 2 mit einer Torte verwechseln",
                     "Player 3 zu Gulasch verarbeiten", "Player 4 mit einer Torte verwechseln",
                     "niemanden die Rei\u00dfz\u00e4hne in den Hals rammen"], "messageId": 0},
                "mode": "write", "target": 2, "highlight": False, "gameId": 2})
        else:
            print("game 2 should be running")
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                              "fromId": 3, "gameId": gameId})

            self.assertReceiveDict({"eventType": "message", "message":
                {"text": ("Die Werw\u00f6lfe suchen ihr Opfer aus.\n\nPlayer 3 schl\u00e4gt vor "
                          "Player 1 in die Lasagne zu mischen.\n\nDie Werw\u00f6lfe haben "
                          "beschlossen, Player 1 in die Lasagne zu mischen."), "messageId": 22},
                "mode": "edit", "target": 2, "highlight": False, "gameId": gameId})

            self.sc.sendJSON({"commandType": "terminate", "fromId": 42,
                              "gameId": gameId})
            self.clearRecBuffer()
