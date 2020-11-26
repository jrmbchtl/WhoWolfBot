from src.systemtest.Systemtest import Systemtest


class BerserkTest3(Systemtest):

    def getName(self):
        return "BerserkTest3"

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
        self.sc.sendJSON({"commandType": "add", "add": {"role": "Berserker"},
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
        self.assertReceiveDict({'eventType': 'choiceField', 'choiceField':
            {'text': 'Du hast noch 2 Leben.\n\nWen greifst du diese Nacht im Rausch an?',
            'options': ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'niemanden'],
            'messageId': 0}, 'mode': 'write', 'target': 2, 'highlight': False, 'gameId': gameId,
            'lang': 'DE'})
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 2}, "fromId": 2,
                          "gameId": gameId})
        self.assertAnyMessage()
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': 'Player 2 hat leider ins Gras gebissen.', 'messageId': 0}, 'mode': 'write',
            'target': 0, 'highlight': True, 'gameId': gameId, 'lang': 'DE'})
        self.assertAnyMessage()
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': 'Player 3 wird nie wieder an den Freuden des Dorfes teilhaben.',
             'messageId': 0}, 'mode': 'write', 'target': 0, 'highlight': True, 'gameId': gameId,
            'lang': 'DE'})
        self.assertAnyMessage()
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': ('Die Dorfbewohner veranstalten zur Feier des Tages einen Fest und stopfen '
                      'den letzten Werwolf aus.'), 'messageId': 0}, 'mode': 'write', 'target': 0,
            'highlight': True, 'gameId': gameId, 'lang': 'DE'})

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
