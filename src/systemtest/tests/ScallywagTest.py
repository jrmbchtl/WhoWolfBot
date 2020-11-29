from src.systemtest.Systemtest import Systemtest


class ScallywagTest(Systemtest):

    def getName(self):
        return "ScallywagTest"

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
        self.sc.sendJSON({"commandType": "add", "add": {"role": "Superschurke"},
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
            {'text': 'Wessen Kissen tauschst du diese Nacht gegen die herzförmige Bombe aus?',
             'options': ['Player 1', 'Player 2', 'Player 3', 'Player 4'], 'messageId': 0},
            'mode': 'write', 'target': 2, 'highlight': False, 'gameId': gameId, 'lang': 'DE'})
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 2,
                          "gameId": gameId})
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': ('Wessen Kissen tauschst du diese Nacht gegen die herzförmige Bombe aus?\n\n'
                      'Du hast Player 2s Kissen mit der herzförmigen Bombe ausgetauscht.'),
             'messageId': 32}, 'mode': 'edit', 'target': 2, 'highlight': False, 'gameId': gameId,
            'lang': 'DE'})
        self.assertAnyMessage()
        for i in range(1, 4):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": i}, "fromId": i,
                              "gameId": gameId})
            self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        for i in range(1, 5):
            self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 2}, "fromId": i,
                              "gameId": gameId})
            self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1}, "fromId": 3,
                          "gameId": gameId})
        self.assertAnyMessage()
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': 'Player 2 ist über die Wupper gegangen.', 'messageId': 0}, 'mode': 'write',
            'target': 0, 'highlight': True, 'gameId': gameId, 'lang': 'DE'})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertReceiveDict({'eventType': 'message', 'message':
            {'text': 'Mit dem Tod des letzten Werwolfes haben die Dorfbewohner jetzt ihre Ruhe.',
             'messageId': 0}, 'mode': 'write', 'target': 0, 'highlight': True, 'gameId': gameId,
            'lang': 'DE'})

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
