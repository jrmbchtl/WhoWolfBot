from src.systemtest.Systemtest import Systemtest


class DoublePattTest(Systemtest):

    def getName(self):
        return "DoublePattTest"

    def run(self):
        gameId = self.initGame(numberOfPlayers=4, admin=42)

        self.assertAnyMessage()
        self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 3, "choiceIndex": 0},
                          "origin": 0, "gameId": gameId})

        for i in range(0, 2):
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 3, "choiceIndex": 0},
                          "origin": 0, "gameId": gameId})

        for i in range(0, 3):
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 3, "choiceIndex": 3},
                          "origin": 0, "gameId": gameId})

        for i in range(0, 2):
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        for i in range(1, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": i, "choiceIndex": i},
                              "origin": 0, "gameId": gameId})
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.assertAnyMessage()
        self.verifyMessage(gameId)
        self.assertAnyMessage()
        self.verifyMessage(gameId)

        for i in range(0, 2):
            self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": i + 1, "choiceIndex": 0},
                              "origin": 0, "gameId": gameId})
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        for i in range(2, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": i + 1, "choiceIndex": 1},
                              "origin": 0, "gameId": gameId})
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.verifyMessage(gameId)
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.verifyMessage(gameId)

        for i in range(0, 2):
            self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": i + 1, "choiceIndex": 0},
                              "origin": 0, "gameId": gameId})
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        for i in range(2, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": i + 1, "choiceIndex": 1},
                              "origin": 0, "gameId": gameId})
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        for i in range(0, 2):
            self.assertAnyMessage()
            self.verifyMessage(gameId)

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Nach einem anstrengenden Tag hoffen viele Dorfbewohner nun auf eine "
                      "erholsame Nacht. Doch diese Nacht werden nicht alle gut schlafen..."),
             "messageId": 0}, "mode": "write", "target": 0, "highlight": False, "gameId": gameId})
        self.verifyMessage(gameId)

        self.sc.sendJSON({"commandType": "terminate", "terminate": {"fromId": 42},
                          "gameId": gameId})
        self.clearRecBuffer()
