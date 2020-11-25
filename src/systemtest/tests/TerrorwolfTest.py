from src.systemtest.Systemtest import Systemtest


class TerrorwolfTest(Systemtest):

    def getName(self):
        return "TerrorwolfTest"

    def run(self):
        gameId = self.initGame(6, 42, 1)

        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Welche Gene setzen sich in dir durch?",
             "options": ['dem Dorf den Rücken zuwenden', 'Humanität zeigen'], "messageId": 0},
            "mode": "write", "target": 3, "highlight": False, "gameId": gameId, 'lang': 'DE'})

        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 3, "gameId": gameId})

        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Welche Gene setzen sich in dir durch?\n\n"
                      "Du hast dem Dorf den Rücken zugewendet."),
             "messageId": 32}, "mode": "edit", "target": 3, "highlight": False, "gameId": gameId,
            'lang': 'DE'})
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Frischer Mensch - kommt auf den Tisch - so saftig süüüüüüüüüüüüüüüß!",
             "options":
                ['Player 1 durch den Fleischwolf jagen', 'Player 2 zu Salami verarbeiten',
                 'Player 3 zu Gulasch verarbeiten', 'Player 4 versnacken', 'Player 5 reißen',
                 'Player 6 reißen', 'niemanden reißen'],
             "messageId": 0}, "mode": "write", "target": 3, "highlight": False, "gameId": gameId,
            'lang': 'DE'})
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Frischer Mensch - kommt auf den Tisch - so saftig süüüüüüüüüüüüüüüß!",
             "options":
             ['Player 1 durch den Fleischwolf jagen', 'Player 2 zu Salami verarbeiten',
              'Player 3 zu Gulasch verarbeiten', 'Player 4 versnacken', 'Player 5 reißen',
              'Player 6 reißen', 'niemanden reißen'],
             "messageId": 0}, "mode": "write", "target": 4, "highlight": False, "gameId": gameId,
            'lang': 'DE'})
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 3},
                          "fromId": 3, "gameId": gameId})
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": ("Frischer Mensch - kommt auf den Tisch - so saftig süüüüüüüüüüüüüüüß!\n\n"
                      "Player 3 schlägt vor Player 4 zu versnacken.\n"), "options":
                ['Player 1 durch den Fleischwolf jagen', 'Player 2 zu Salami verarbeiten',
                 'Player 3 zu Gulasch verarbeiten', 'Player 4 versnacken', 'Player 5 reißen',
                 'Player 6 reißen', 'niemanden reißen'],
             "messageId": 34}, "mode": "edit", "target": 3, "highlight": False, "gameId": gameId,
            'lang': 'DE'})
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": ("Frischer Mensch - kommt auf den Tisch - so saftig süüüüüüüüüüüüüüüß!\n\n"
                      "Player 3 schlägt vor Player 4 zu versnacken.\n"), "options":
                ['Player 1 durch den Fleischwolf jagen', 'Player 2 zu Salami verarbeiten',
                 'Player 3 zu Gulasch verarbeiten', 'Player 4 versnacken', 'Player 5 reißen',
                 'Player 6 reißen', 'niemanden reißen'],
             "messageId": 35}, "mode": "edit", "target": 4, "highlight": False, "gameId": gameId,
            'lang': 'DE'})
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 3},
                          "fromId": 4, "gameId": gameId})
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Frischer Mensch - kommt auf den Tisch - so saftig süüüüüüüüüüüüüüüß!\n\n"
                      "Player 3 schlägt vor Player 4 zu versnacken.\nPlayer 4 schlägt vor Player 4 "
                      "zu versnacken.\n\nDie Werwölfe haben beschlossen, Player 4 zu versnacken."),
             "messageId": 34}, "mode": "edit", "target": 3, "highlight": False, "gameId": gameId,
            'lang': 'DE'})
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": ("Frischer Mensch - kommt auf den Tisch - so saftig süüüüüüüüüüüüüüüß!\n\n"
                      "Player 3 schlägt vor Player 4 zu versnacken.\nPlayer 4 schlägt vor Player 4 "
                      "zu versnacken.\n\nDie Werwölfe haben beschlossen, Player 4 zu versnacken."),
             "messageId": 35}, "mode": "edit", "target": 4, "highlight": False, "gameId": gameId,
            'lang': 'DE'})
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": ("Player 4 wurde diese Nacht von den Werw\u00f6lfen erwischt. M\u00f6chtest "
                      "du diese Person retten?"), "options":
                ['Wiederbeleben', 'Sterben lassen'], "messageId": 0},
            "mode": "write", "target": 2, "highlight": False, "gameId": gameId, 'lang': 'DE'})
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 1},
                          "fromId": 2, "gameId": gameId})
        self.assertAnyMessage()
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Du hast Player 4 sterben gelassen.", "messageId": 0},
            "mode": "write", "target": 2, "highlight": False, "gameId": gameId, 'lang': 'DE'})
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Willst du noch jemanden t\u00f6ten?", "options":
                ['Player 1 ausversehen Gift in das Getränk mischen',
                 'Player 3 ausversehen eine Überdosis Morphium verabreichen',
                 'Player 4 ausversehen Gift in das Getränk mischen', 'Player 5 vergiften',
                 'Player 6 einen Kugelfisch falsch zubereiten',
                 'Niemanden ausversehen eine Überdosis Morphium verabreichen'],
             "messageId": 0}, "mode": "write", "target": 2, "highlight": False, "gameId": gameId,
            'lang': 'DE'})
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 5},
                          "fromId": 2, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 5, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 4 bei\u00dft einen Dorfbewohner!", "messageId": 0},
            "mode": "write", "target": 0, "highlight": False, "gameId": gameId, 'lang': 'DE'})
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Wen willst du als letzten Akt zerrei\u00dfen?",
             "options": ["Player 1", "Player 2", "Player 3", "Player 5", "Player 6"],
             "messageId": 0}, "mode": "write", "target": 4, "highlight": False, "gameId": gameId,
            'lang': 'DE'})
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 4, "gameId": gameId})
        self.assertAnyMessage()
        self.assertReceiveDict({"eventType": "message", "message":
            {"text": "Player 1 wurde noch kurz verputzt.",
             "messageId": 0}, "mode": "write", "target": 0, "highlight": True, "gameId": gameId,
            'lang': 'DE'})
        self.assertAnyMessage()

        self.sc.sendJSON({"commandType": "terminate", "fromId": 42, "gameId": gameId})
        self.clearRecBuffer()
