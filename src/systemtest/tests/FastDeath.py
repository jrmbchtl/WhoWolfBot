from src.systemtest.Systemtest import Systemtest


class FastDeath(Systemtest):

    def getName(self):
        return "FastDeath"

    def run(self):
        gameId = self.initGame()

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Die Werwolfsmägen knurren vor Hunger - Zeit, sich etwas zu Essen zu suchen!",
             "options": ['Player 1 reißen', 'Player 2 zu Gulasch verarbeiten',
                         'Player 3 durch den Fleischwolf jagen',
                         'Player 4 durch den Fleischwolf jagen',
                         'niemanden die Reißzähne in den Hals rammen'],
             "messageId": 0}, "mode": "write", "target": 3, "highlight": False, "gameId": gameId,
                                'lang': 'DE'})

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 3, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Die Werwolfsmägen knurren vor Hunger - Zeit, sich etwas zu Essen zu suchen!"
                      "\n\nPlayer 3 schlägt vor Player 1 zu reißen.\n\n"
                      "Die Werwölfe haben beschlossen, Player 1 zu reißen."),
             "messageId": 24}, "mode": "edit", "target": 3, "highlight": False, "gameId": gameId,
                                'lang': 'DE'})

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": ("Player 1 wurde diese Nacht von den Werw\u00f6lfen erwischt. M\u00f6chtest "
                      "du diese Person retten?"), "options":
                ['Retten', 'Ausversehen zu spät kommen'], "messageId": 0},
            "mode": "write", "target": 4, "highlight": False, "gameId": gameId, 'lang': 'DE'})

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1},
                          "fromId": 4, "gameId": gameId})
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Player 1 wurde diese Nacht von den Werw\u00f6lfen erwischt. M\u00f6chtest "
                      "du diese Person retten?"), "messageId": 26}, "mode": "edit", "target": 4,
            "highlight": False, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Du bist für Player 1 ausversehen zu spät gekommen.",
             "messageId": 0}, "mode": "write", "target": 4,
            "highlight": False, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Willst du noch jemanden t\u00f6ten?",
             "options": ['Player 1 einen Kugelfisch falsch zubereiten',
                         'Player 2 ausversehen Gift in das Getränk mischen',
                         'Player 3 ausversehen eine Überdosis Morphium verabreichen',
                         'Niemanden ein Essen mit Fliegenpilzen zubereiten'],
             "messageId": 0}, "mode": "write", "target": 4, "highlight": False, "gameId": gameId,
                                'lang': 'DE'})

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 2},
                          "fromId": 4, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Willst du noch jemanden t\u00f6ten?", "messageId": 29},
            "mode": "edit", "target": 4, "highlight": False, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Du hast Player 3 eine Überdosis Morphium verabreicht.", "messageId": 0},
            "mode": "write", "target": 4, "highlight": False, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 1 hat den Löffel abgegeben.", "messageId": 0},
            "mode": "write", "target": 0, "highlight": True, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 1 hat den Löffel abgegeben.", "messageId": 0},
            "mode": "write", "target": 1, "highlight": True, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Player 1 versucht mit Waffengewalt, kurz vor seinem Tod noch für "
                      "Gerechtigkeit zu sorgen!"), "messageId": 0},
            "mode": "write", "target": 0, "highlight": False, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Wen möchtest du mit ins Grab nehmen?", "options":
                ['Player 2 durchlöchern', 'Player 4 niederstrecken'],
             "messageId": 0}, "mode": "write", "target": 1, "highlight": False, "gameId": gameId,
                                'lang': 'DE'})

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 1, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Wen möchtest du mit ins Grab nehmen?", "messageId": 35},
            "mode": "edit", "target": 1, "highlight": False, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 2 hat nun sehr viele Löcher in Kopf und Brust.", "messageId": 0},
            "mode": "write", "target": 0, "highlight": True, "gameId": gameId, 'lang': 'DE'})
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 2 hat nun sehr viele Löcher in Kopf und Brust.", "messageId": 0},
            "mode": "write", "target": 2, "highlight": True, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 3 hat die letzten Stunden nicht überlebt.", "messageId": 0},
            "mode": "write", "target": 0, "highlight": True, "gameId": gameId, 'lang': 'DE'})
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 3 hat die letzten Stunden nicht überlebt.", "messageId": 0},
            "mode": "write", "target": 3, "highlight": True, "gameId": gameId, 'lang': 'DE'})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Es wird wieder friedlich in Düsterwald, da hier nur noch Dorfbewohner "
                      "leben."), "messageId": 0},
            "mode": "write", "target": 0, "highlight": True, "gameId": gameId, 'lang': 'DE'})

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
