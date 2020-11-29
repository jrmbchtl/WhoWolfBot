from src.systemtest.Systemtest import Systemtest


class BadassBastardTest(Systemtest):

    def getName(self):
        return "BadassBastardTest"

    def run(self):
        self.sc.sendJSON({"commandType": "newGame", "newGame": {"origin": 0, "seed": 0},
                          "fromId": 42})
        rec = self.assertAnyMessage()
        gameId = rec["gameId"]
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 42,
                          "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        remList = ["Jäger", "Seherin", "Terrorwolf", "Hexe", "Wolfshund"]
        for role in remList:
            self.sc.sendJSON({"commandType": "remove", "remove": {"role": role}, "fromId": 42,
                              "gameId": gameId})
            self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "add", "add": {"role": "Harter\xa0Bursche"},
                          "fromId": 42, "gameId": gameId})
        self.assertAnyMessage()
        for i in range(1, 5):
            self.sc.sendJSON({"commandType": "register", "register":
                {"name": "Player " + str(i)}, "fromId": i, "gameId": gameId})
            for j in range(0, 3):
                self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "startGame", "fromId": 42, "gameId": gameId})
        for i in range(0, 8):
            self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 3,
                          "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        for i in range(0, 3):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": i}, "fromId": i + 1,
                              "gameId": gameId})
            self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        for i in range(0, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": i + 1,
                              "gameId": gameId})
            self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 3,
                          "gameId": gameId})
        self.assertAnyMessage()
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': 'Player 2 besucht nun die ewigen Jagdgründe.', 'messageId': 0},
            'mode': 'write', 'target': 0, 'highlight': True, 'gameId': gameId,
            'lang': 'DE'})

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
