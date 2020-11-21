from src.systemtest.Systemtest import Systemtest


class DoublePattTest(Systemtest):

    def getName(self):
        return "DoublePattTest"

    def run(self):
        gameId = self.initGame(numberOfPlayers=4, admin=42)

        self.assertAnyMessage()

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 3, "gameId": gameId})

        for i in range(0, 2):
            self.assertAnyMessage()

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 4, "gameId": gameId})

        for i in range(0, 3):
            self.assertAnyMessage()

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 3},
                          "fromId": 4, "gameId": gameId})

        for i in range(0, 2):
            self.assertAnyMessage()

        for i in range(1, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": i},
                              "fromId": i, "gameId": gameId})
            self.assertAnyMessage()

        self.assertAnyMessage()
        self.assertAnyMessage()

        for i in range(0, 2):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                              "fromId": i + 1, "gameId": gameId})
            self.assertAnyMessage()

        for i in range(2, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1},
                              "fromId": i + 1, "gameId": gameId})
            self.assertAnyMessage()

        self.assertAnyMessage()
        self.assertAnyMessage()

        for i in range(0, 2):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                              "fromId": i + 1, "gameId": gameId})
            self.assertAnyMessage()

        for i in range(2, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1},
                              "fromId": i + 1, "gameId": gameId})
            self.assertAnyMessage()

        for i in range(0, 2):
            self.assertAnyMessage()

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Nach einem anstrengenden Tag hoffen viele Dorfbewohner nun auf eine "
                      "erholsame Nacht. Doch diese Nacht werden nicht alle gut schlafen..."),
             "messageId": 0}, "mode": "write", "target": 0, "highlight": False, "gameId": gameId,

                                'lang': 'DE'})

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
