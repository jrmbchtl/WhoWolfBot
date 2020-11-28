from src.systemtest.Systemtest import Systemtest


class PsychopathTest(Systemtest):

    def getName(self):
        return "PsychopathTest"

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
        self.sc.sendJSON({"commandType": "add", "add": {"role": "Psychopath"},
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
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 4}, "fromId": 3,
                          "gameId": gameId})
        self.assertAnyMessage()
        self.assertReceiveDict({'eventType': 'choiceField', 'choiceField':
            {'text': 'In den frühen Morgenstunden machst du dich auf und suchst dein Opfer...',
             'options': ['Player 1 in den Backofen stecken', 'Player 2 kaltblütig zerstückeln',
                         'Player 3 von einer Klippe stoßen', 'Player 4 ermorden'], 'messageId': 0},
            'mode': 'write', 'target': 2, 'highlight': False, 'gameId': gameId, 'lang': 'DE'})
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0}, "fromId": 2,
                          "gameId": gameId})
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': ('In den frühen Morgenstunden machst du dich auf und suchst dein Opfer...\n\n'
                      'Der Psychopath hat Player 1 in den Backofen gesteckt.'), 'messageId': 32},
            'mode': 'edit', 'target': 2, 'highlight': False, 'gameId': gameId, 'lang': 'DE'})
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': 'Player 1 hat leider ins Gras gebissen.', 'messageId': 0}, 'mode': 'write',
            'target': 0, 'highlight': True, 'gameId': gameId, 'lang': 'DE'})

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
