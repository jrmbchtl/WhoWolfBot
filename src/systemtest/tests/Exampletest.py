from src.systemtest.Systemtest import Systemtest


class Exampletest(Systemtest):

    def getName(self):
        return "Exampletest"

    def run(self):
        print("running Exampletest")
        self.sc.sendJSON({"commandType": "newGame", "newGame": {"origin": 0}, "fromId": 42})
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": ("Viel Spass beim Werwolf spielen!\n\nBitte einen privaten Chat mit dem Bot "
                      "starten, bevor das Spiel beginnt!\n\nUm das Spiel in seiner vollen Breite "
                      "genie\u00dfen zu k\u00f6nnen, empfiehlt es sich bei sehr schmalen "
                      "Bildschirmen, diese quer zu verwenden.\n\nSpieler:\n"),
             "options": ["Mitspielen/Aussteigen", "Start", "Abbrechen"],
             "messageId": 0}, "mode": "write", "target": 0, "highlight": False, "gameId": 1})

        self.verifyMessage(1)
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Hier k\u00f6nnen Rollen hinzugef\u00fcgt oder entfernt werden",
             "options": ["wolfshund deaktivieren", "terrorwolf deaktivieren",
                         "seherin deaktivieren", "hexe deaktivieren", "jaeger deaktivieren"],
             "messageId": 0}, "mode": "write", "target": 42, "highlight": False, "gameId": 1})
        self.verifyMessage(1)
        self.sc.sendJSON({"commandType": "startGame", "fromId": 42, "gameId": 1})
        for i in range(1, 5):
            self.sc.sendJSON({"commandType": "register", "register":
                             {"name": "Player " + str(i)}, "fromId": i, "gameId": 1})
            self.assertAnyMessage()
            self.verifyMessage(1)
            self.assertAnyMessage()
            self.verifyMessage(1)
            self.assertAnyMessage()
            self.verifyMessage(1)
        self.sc.sendJSON({"commandType": "startGame", "fromId": 42, "gameId": 1})
        self.assertAnyMessage()
        self.verifyMessage(1)
        self.assertAnyMessage()
        self.verifyMessage(1)
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Du bist einer der Werw\u00f6lfe. Diese suchen sich jede Nacht gemeinsam ein "
                      "Opfer aus, welches sie t\u00f6ten wollen. Ihr Ziel ist es, dass nur "
                      "Charaktere der Werw\u00f6lfe \u00fcberleben."), "messageId": 0},
            "mode": "write", "target": 3, "highlight": False, "gameId": 1})
        self.verifyMessage(1)
        self.assertReceiveDict({"eventType": "message", "message":
            {'text': ("Du bist die Hexe. Diese erwacht jede Nacht, erfährt das Opfer der Werwölfe "
                      "und darf sich entscheiden, ob sie ihren einen Lebenstrank auf das Opfer "
                      "anwendet. Anschließend hat sie die Möglichkeit, einmal im Spiel eine Person "
                      "mit einem Todestrank zu ermorden."), "messageId": 0},
            "mode": "write", "target": 2, "highlight": False, "gameId": 1})
        self.verifyMessage(1)
        self.assertReceiveDict({"eventType": "message", "message":
            {'text': ("Du bist der Jäger. Wenn der Jäger stirbt, muss er noch einen Spieler "
                      "seiner Wahl in den Tod mitnehmen."), "messageId": 0},
            "mode": "write", "target": 4, "highlight": False, "gameId": 1})
        self.verifyMessage(1)
        self.assertReceiveDict({"eventType": "message", "message":
            {'text': ('Du bist ein Dorfbewohner, ein normaler Charakter mit keinerlei besonderen '
                      'Fähigkeiten.'), 'messageId': 0},
            "mode": "write", "target": 1, "highlight": False, "gameId": 1})
        self.verifyMessage(1)
        self.assertAnyMessage()
        self.verifyMessage(1)

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": 1})
        self.clearRecBuffer()
