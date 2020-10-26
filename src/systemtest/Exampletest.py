from .Systemtest import Systemtest


class Exampletest(Systemtest):

    def run(self):
        print("running Exampletest")
        self.sc.sendJSON({"commandType": "newGame", "newGame": {"senderId": 42}, "origin": 1})
        self.asserReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": ("Viel Spass beim Werwolf spielen!\n\nBitte einen privaten Chat mit dem Bot "
                      "starten, bevor das Spiel beginnt!\n\nUm das Spiel in seiner vollen Breite "
                      "genie\u00dfen zu k\u00f6nnen, empfiehlt es sich bei sehr schmalen "
                      "Bildschirmen, diese quer zu verwenden.\n\nSpieler:\n"),
             "options": ["Mitspielen/Aussteigen", "Start", "Cancel"],
             "messageId": 0}, "mode": ["write"], "target": 1, "gameId": 1})
        self.sc.sendJSON({"commandType": "startGame", "startGame": {"senderId": 42},
                          "origin": 1, "gameId": 1})
        self.sc.sendJSON({"commandType": "register", "register": {"name": "player 1", "id": 1},
                          "origin": 1, "gameId": 1})
        self.sc.sendJSON({"commandType": "register", "register": {"name": "player 2", "id": 1},
                          "origin": 1, "gameId": 1})
        self.sc.sendJSON({"commandType": "register", "register": {"name": "player 3", "id": 1},
                          "origin": 1, "gameId": 1})
        self.sc.sendJSON({"commandType": "register", "register": {"name": "player 4", "id": 1},
                          "origin": 1, "gameId": 1})
        self.sc.sendJSON({"commandType": "startGame", "startGame": {"senderId": 42},
                          "origin": 1, "gameId": 1})
        self.asserReceiveDict({"eventType": "gameStarted", "gameId": 1})
