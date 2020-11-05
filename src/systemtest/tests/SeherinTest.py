from src.systemtest.Systemtest import Systemtest


class SeherinTest(Systemtest):

    def getName(self):
        return "SeherinTest"

    def run(self):
        gameId = self.initGame(5, 42, 1)

        self.assertAnyMessage()
        self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 3, "choiceIndex": 0},
                          "origin": 0, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(gameId)
        self.assertAnyMessage()
        self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 4, "choiceIndex": 0},
                          "origin": 0, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "terminate", "terminate": {"fromId": 42},
                          "gameId": gameId})
        self.clearRecBuffer()
