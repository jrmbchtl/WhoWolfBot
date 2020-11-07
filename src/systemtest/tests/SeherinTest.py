from src.systemtest.Systemtest import Systemtest


class SeherinTest(Systemtest):

    def getName(self):
        return "SeherinTest"

    def run(self):
        gameId = self.initGame(5, 42, 1)

        self.assertAnyMessage()
        self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 3, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(gameId)
        self.assertAnyMessage()
        self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 4, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
