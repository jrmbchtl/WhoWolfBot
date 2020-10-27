from src.systemtest.Systemtest import Systemtest


class Exampletest(Systemtest):

    def run(self):
        print("running Exampletest")
        self.sc.sendJSON({"commandType": "newGame", "newGame": {"senderId": 42}, "origin": 0})
        self.asserReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": ("Viel Spass beim Werwolf spielen!\n\nBitte einen privaten Chat mit dem Bot "
                      "starten, bevor das Spiel beginnt!\n\nUm das Spiel in seiner vollen Breite "
                      "genie\u00dfen zu k\u00f6nnen, empfiehlt es sich bei sehr schmalen "
                      "Bildschirmen, diese quer zu verwenden.\n\nSpieler:\n"),
             "options": ["Mitspielen/Aussteigen", "Start", "Cancel"],
             "messageId": 0}, "mode": ["write"], "target": 0, "gameId": 1})

        self.verifyMessage(112, 1)
        self.sc.sendJSON({"commandType": "startGame", "startGame": {"senderId": 42},
                          "origin": 0, "gameId": 1})
        for i in range(1, 5):
            self.sc.sendJSON({"commandType": "register", "register":
                             {"name": "Player " + str(i), "id": i}, "origin": 0, "gameId": 1})
            self.assertAnyMessage()
            self.verifyMessage()
            self.assertAnyMessage()
            self.verifyMessage()
            self.assertAnyMessage()
            self.verifyMessage()
        self.sc.sendJSON({"commandType": "startGame", "startGame": {"senderId": 42},
                          "origin": 0, "gameId": 1})
        self.assertAnyMessage()
        self.verifyMessage()
        self.asserReceiveDict({"eventType": "message", "message":
            {"text": ("Du bist einer der Werw\u00f6lfe. Diese suchen sich jede Nacht gemeinsam ein "
                      "Opfer aus, welches sie t\u00f6ten wollen. Ihr Ziel ist es, dass nur "
                      "Charaktere der Werw\u00f6lfe \u00fcberleben."), "messageId": 0},
            "mode": ["write"], "target": 3, "gameId": 1})
        self.verifyMessage()
        self.asserReceiveDict({"eventType": "message", "message":
            {'text': ("Du bist die Hexe. Diese erwacht jede Nacht, erfährt das Opfer der Werwölfe "
                      "und darf sich entscheiden, ob sie ihren einen Lebenstrank auf das Opfer "
                      "anwendet. Anschließend hat sie die Möglichkeit, einmal im Spiel eine Person "
                      "mit einem Todestrank zu ermorden."), "messageId": 0},
            "mode": ["write"], "target": 2, "gameId": 1})
        self.verifyMessage()
        self.asserReceiveDict({"eventType": "message", "message":
            {'text': ("Du bist der Jäger. Wenn der Jäger stirbt, muss er noch einen Spieler "
                      "seiner Wahl in den Tod mitnehmen."), "messageId": 0},
            "mode": ["write"], "target": 4, "gameId": 1})
        self.verifyMessage()
        self.asserReceiveDict({"eventType": "message", "message":
            {'text': ('Du bist ein Dorfbewohner, ein normaler Charakter mit keinerlei besonderen '
                      'Fähigkeiten.'), 'messageId': 0},
            "mode": ["write"], "target": 1, "gameId": 1})
        self.verifyMessage()
        self.assertAnyMessage()
        self.verifyMessage()