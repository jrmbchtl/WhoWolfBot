from src.systemtest.Systemtest import Systemtest


class WhiteWolfTest(Systemtest):

    def getName(self):
        return "WhiteWolfTest"

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
        self.sc.sendJSON({"commandType": "add", "add": {"role": "Weißer\xa0Wolf"},
                          "fromId": 42, "gameId": gameId})
        self.assertAnyMessage()
        for i in range(1, 7):
            self.sc.sendJSON({"commandType": "register", "register":
                {"name": "Player " + str(i)}, "fromId": i, "gameId": gameId})
            for j in range(0, 3):
                self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "startGame", "fromId": 42, "gameId": gameId})
        for i in range(0, 11):
            self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 5, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 3, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1},
                          "fromId": 3, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        for i in range(2, 5):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": i - 2},
                              "fromId": i, "gameId": gameId})
            self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        for i in range(2, 7):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                              "fromId": i, "gameId": gameId})
            self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 3},
                          "fromId": 5, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 3},
                          "fromId": 3, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        for i in range(3, 6):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1},
                              "fromId": i, "gameId": gameId})
            self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 2},
                          "fromId": 3, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 2},
                          "fromId": 5, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 3, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': ('Es gibt keine Dorfbewohner und keine normalen Werwölfe mehr, die von den dem'
                      ' weißen Werwolf verspeißt werden können.'), 'messageId': 0}, 'mode': 'write',
            'target': 0, 'highlight': True, 'gameId': gameId, 'lang': 'DE'})

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
