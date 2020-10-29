from src.systemtest.Systemtest import Systemtest


class FastDeath(Systemtest):

    def getName(self):
        return "FastDeath"

    def run(self):
        gameId = self.initGame()

        self.asserReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Mit wem lassen sich die hungrigen Werwolfsm\u00e4uler am besten stopfen?",
             "options": ["Player 1 durch den Fleischwolf jagen",
                         "Player 2 durch den Fleischwolf jagen",
                         "Player 3 die Rei\u00dfz\u00e4hne in den Hals rammen",
                         "Player 4 zu Salami verarbeiten", "niemanden rei\u00dfen"],
             "messageId": 0}, "mode": ["write"], "target": 3, "gameId": 2})
        self.verifyMessage(0, gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 3, "choiceIndex": 0},
                          "origin": 0, "gameId": gameId})

        self.asserReceiveDict({"eventType": "message", "message":
            {"text": ("Mit wem lassen sich die hungrigen Werwolfsm\u00e4uler am besten stopfen?"
                      "\n\nPlayer 3 schl\u00e4gt vor Player 1 durch den Fleischwolf zu jagen.\n"),
             "messageId": 0}, "mode": ["edit"], "target": 3, "gameId": 2})
        self.verifyMessage(0, gameId)

        self.asserReceiveDict({"eventType": "message", "message":
            {"text":
             "Die Werw\u00f6lfe haben beschlossen, Player 1 durch den Fleischwolf zu jagen.",
             "messageId": 0}, "mode": ["write"], "target": 3, "gameId": 2})
        self.verifyMessage(0, gameId)

        self.clearRecBuffer()
        self.sc.sendJSON({"commandType": "terminate", "terminate": {"fromId": 42},
                          "gameId": gameId})
