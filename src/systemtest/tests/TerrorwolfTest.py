from src.systemtest.Systemtest import Systemtest


class TerrorwolfTest(Systemtest):

    def getName(self):
        return "TerrorwolfTest"

    def run(self):
        gameId = self.initGame(6, 42, 1)

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "M\u00f6chtest du Menschen fressen oder von Menschen gelyncht werden?",
             "options": ["Blutlust entwickeln", "harmloser Scho\u00dfhund werden"], "messageId": 0},
            "mode": "write", "target": 3, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)

        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 3, "choiceIndex": 0},
                          "origin": 0, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "M\u00f6chtest du Menschen fressen oder von Menschen gelyncht werden?",
             "messageId": 0}, "mode": "edit", "target": 3, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Du hast Blutlust enwickelt.", "messageId": 0},
            "mode": "write", "target": 3, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Die Werw\u00f6lfe suchen ihr Opfer aus.", "options":
                ["Player 1 mit einer Torte verwechseln", "Player 2 durch den Fleischwolf jagen",
                 "Player 3 zu Salami verarbeiten", "Player 4 zu Gulasch verarbeiten",
                 "Player 5 versnacken", "Player 6 rei\u00dfen", "niemanden rei\u00dfen"],
             "messageId": 0}, "mode": "write", "target": 3, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Die Werw\u00f6lfe suchen ihr Opfer aus.", "options":
                ["Player 1 mit einer Torte verwechseln", "Player 2 durch den Fleischwolf jagen",
                 "Player 3 zu Salami verarbeiten", "Player 4 zu Gulasch verarbeiten",
                 "Player 5 versnacken", "Player 6 rei\u00dfen", "niemanden rei\u00dfen"],
             "messageId": 0}, "mode": "write", "target": 4, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 3, "choiceIndex": 3},
                          "origin": 0, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 4, "choiceIndex": 3},
                          "origin": 0, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": ("Player 4 wurde diese Nacht von den Werw\u00f6lfen erwischt. M\u00f6chtest "
                      "du diese Person retten?"), "options":
                ["Wieder zusammenn\u00e4hen", "Sterben lassen"], "messageId": 0},
            "mode": "write", "target": 1, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 1, "choiceIndex": 1},
                          "origin": 0, "highlight": False, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Du hast Player 4 sterben gelassen.", "messageId": 0},
            "mode": "write", "target": 1, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Willst du noch jemanden t\u00f6ten?", "options":
                ["Player 2 ausversehen Gift in das Getr\u00e4nk mischen",
                 "Player 3 ausversehen eine \u00dcberdosis Morphium verabreichen",
                 "Player 4 ausversehen Gift in das Getr\u00e4nk mischen", "Player 5 vergiften",
                 "Player 6 einen Kugelfisch falsch zubereiten",
                 "Niemanden ausversehen eine \u00dcberdosis Morphium verabreichen"],
             "messageId": 0}, "mode": "write", "target": 1, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 1, "choiceIndex": 5},
                          "origin": 0, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.sc.sendJSON({"commandType": "reply", "reply": {"fromId": 5, "choiceIndex": 0},
                          "origin": 0, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 4 bei\u00dft einen Dorfbewohner!", "messageId": 0},
            "mode": "write", "target": 0, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Wen willst du als letzten Akt zerrei\u00dfen?",
             "options": ["Player 1", "Player 2", "Player 3", "Player 5", "Player 6"],
             "messageId": 0}, "mode": "write", "target": 4, "highlight": False, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.sc.sendJSON({"commandType": "reply", "reply":
            {"fromId": 4, "choiceIndex": 0}, "origin": 0, "highlight": False, "gameId": gameId})
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 1 hat sich im Vorbeilaufen die Z\u00e4hne in den Hals rammen lassen.",
             "messageId": 0}, "mode": "write", "target": 0, "highlight": True, "gameId": gameId})
        self.verifyMessage(0, gameId)
        self.assertAnyMessage()
        self.verifyMessage(0, gameId)

        self.clearRecBuffer()
        self.sc.sendJSON({"commandType": "terminate", "terminate": {"fromId": 42},
                          "gameId": gameId})
