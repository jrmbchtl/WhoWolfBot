from src.systemtest.Systemtest import Systemtest


class PattTest(Systemtest):

    def getName(self):
        return "PattTest"

    def run(self):
        gameId = self.initGame(numberOfPlayers=4, admin=42)

        self.assertAnyMessage()
        self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 3, "gameId": gameId})

        for i in range(0, 2):
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 3, "gameId": gameId})

        for i in range(0, 3):
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 3},
                          "fromId": 3, "gameId": gameId})

        for i in range(0, 2):
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        for i in range(1, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": i},
                              "fromId": i, "gameId": gameId})
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.assertAnyMessage()
        self.verifyMessage(gameId)
        self.assertAnyMessage()
        self.verifyMessage(gameId)

        for i in range(0, 2):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                              "fromId": i + 1, "gameId": gameId})
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        for i in range(2, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1},
                              "fromId": i + 1, "gameId": gameId})
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.verifyMessage(gameId)
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.verifyMessage(gameId)

        for i in range(0, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                              "fromId": i + 1, "gameId": gameId})
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        for i in range(0, 2):
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
