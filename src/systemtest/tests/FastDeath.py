from src.systemtest.Systemtest import Systemtest


class FastDeath(Systemtest):

    def getName(self):
        return "FastDeath"

    def run(self):
        gameId = self.initGame()

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Mit wem lassen sich die hungrigen Werwolfsm\u00e4uler am besten stopfen?",
             "options": ["Player 1 durch den Fleischwolf jagen",
                         "Player 2 durch den Fleischwolf jagen",
                         "Player 3 die Rei\u00dfz\u00e4hne in den Hals rammen",
                         "Player 4 zu Salami verarbeiten", "niemanden rei\u00dfen"],
             "messageId": 0}, "mode": "write", "target": 3, "highlight": False, "gameId": gameId})

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 3, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Mit wem lassen sich die hungrigen Werwolfsm\u00e4uler am besten stopfen?"
                      "\n\nPlayer 3 schl\u00e4gt vor Player 1 durch den Fleischwolf zu jagen.\n\n"
                      "Die Werw\u00f6lfe haben beschlossen, Player 1 durch den Fleischwolf zu "
                      "jagen."),
             "messageId": 22}, "mode": "edit", "target": 3, "highlight": False, "gameId": gameId})

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": ("Player 1 wurde diese Nacht von den Werw\u00f6lfen erwischt. M\u00f6chtest "
                      "du diese Person retten?"), "options":
                ["Heilen", "Lebenstrank nicht f\u00fcr sojemanden verschwenden"], "messageId": 0},
            "mode": "write", "target": 2, "highlight": False, "gameId": gameId})

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1},
                          "fromId": 3, "gameId": gameId})
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Player 1 wurde diese Nacht von den Werw\u00f6lfen erwischt. M\u00f6chtest "
                      "du diese Person retten?"), "messageId": 24}, "mode": "edit", "target": 2,
            "highlight": False, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Die Hexe wollte ihren Lebenstrank nicht f\u00fcr jemanden wie Player 1 "
                      "verschwenden."), "messageId": 0}, "mode": "write", "target": 2,
            "highlight": False, "gameId": gameId})

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Willst du noch jemanden t\u00f6ten?",
             "options": ['Player 1 ausversehen eine Überdosis Morphium verabreichen',
                         'Player 3 ein Essen mit Fliegenpilzen zubereiten',
                         'Player 4 Quecksilber in die Milch mischen',
                         'Niemanden mit radioaktivem Gemüse versorgen'],
             "messageId": 0}, "mode": "write", "target": 2, "highlight": False, "gameId": gameId})

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 2},
                          "fromId": 2, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Willst du noch jemanden t\u00f6ten?", "messageId": 27},
            "mode": "edit", "target": 2, "highlight": False, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Die Hexe hat Player 4 Quecksilber in die Milch gemischt.", "messageId": 0},
            "mode": "write", "target": 2, "highlight": False, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 1 ist von uns gegangen.", "messageId": 0},
            "mode": "write", "target": 0, "highlight": True, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 1 ist von uns gegangen.", "messageId": 0},
            "mode": "write", "target": 1, "highlight": True, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 4 ist \u00fcber die Wupper gegangen.", "messageId": 0},
            "mode": "write", "target": 0, "highlight": True, "gameId": gameId})
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 4 ist \u00fcber die Wupper gegangen.", "messageId": 0},
            "mode": "write", "target": 4, "highlight": True, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 4 war der J\u00e4ger!", "messageId": 0},
            "mode": "write", "target": 0, "highlight": False, "gameId": gameId})

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Wen willst du wegpusten?", "options":
                ["Player 2 niederstrecken", "Player 3 in der Notwehr erschie\u00dfen"],
             "messageId": 0}, "mode": "write", "target": 4, "highlight": False, "gameId": gameId})

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 4, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Wen willst du wegpusten?", "messageId": 35},
            "mode": "edit", "target": 4, "highlight": False, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 2 wurde niedergestreckt.", "messageId": 0},
            "mode": "write", "target": 0, "highlight": True, "gameId": gameId})
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 2 wurde niedergestreckt.", "messageId": 0},
            "mode": "write", "target": 2, "highlight": True, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Es wird wieder friedlich in D\u00fcsterwald, da hier jetzt nur noch "
                      "Werw\u00f6lfe leben."), "messageId": 0},
            "mode": "write", "target": 0, "highlight": True, "gameId": gameId})

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
