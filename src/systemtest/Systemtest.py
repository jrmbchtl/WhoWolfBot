import time

from src.main.client.conn.ServerConnection import ServerConnection
from multiprocessing import Process


class Systemtest(object):
    def __init__(self, sc):
        super(Systemtest, self)
        self.sc: ServerConnection = sc
        self.messageId = 1

    def getName(self):
        raise NameError("You should name your test!")

    def run(self):
        pass

    def assertReceiveDict(self, dc):
        rec = self.sc.receiveJSON()
        self.dictCompare(dc, rec)
        self.__verifyMessage(rec["gameId"], rec["target"])

    def assertAnyMessage(self):
        rec = self.sc.receiveJSON()
        self.__verifyMessage(rec["gameId"], rec["target"])

    def __verifyMessage(self, gameId, fromId):
        self.sc.sendJSON({"commandType": "feedback", "feedback":
            {"success": 1, "messageId": self.messageId}, "fromId": fromId, "gameId": gameId})
        self.messageId += 1

    def dictCompare(self, expected, actual):
        for key in expected:
            assertIn(key, actual)
            if isinstance(expected[key], dict):
                self.dictCompare(expected[key], actual[key])
            else:
                assertEqual(expected[key], actual[key])
        for key in actual:
            assertIn(key, expected)
            if isinstance(actual[key], dict):
                self.dictCompare(expected[key], actual[key])
            else:
                assertEqual(expected[key], actual[key])

    # handles everything including nightfall and returns the gameId
    def initGame(self, numberOfPlayers=4, admin=42, seed=42):
        self.sc.sendJSON({"commandType": "newGame", "newGame": {"origin": 0, "seed": seed},
                          "fromId": admin})
        rec = self.sc.receiveJSON()
        gameId = rec["gameId"]
        self.__verifyMessage(gameId, rec["target"])
        self.sc.sendJSON({"commandType": "reply", "reply": {"choiceIndex": 0},
                          "fromId": 42, "gameId": gameId})
        self.assertAnyMessage()
        self.assertAnyMessage()
        self.assertReceiveDict({"eventType": "choiceField", "choiceField":
            {"text": "Hier k\u00f6nnen Rollen hinzugef\u00fcgt oder entfernt werden",
             "options": ['Jäger deaktivieren', 'Seherin deaktivieren', 'Terrorwolf deaktivieren',
                         'Hexe deaktivieren', 'Wolfshund deaktivieren'],
             "messageId": 0}, "mode": "write", "target": 42, "highlight": False, "gameId": gameId,
            "lang": "DE"})
        for i in range(1, numberOfPlayers + 1):
            self.sc.sendJSON({"commandType": "register", "register":
                {"name": "Player " + str(i)}, "fromId": i, "gameId": gameId})
            for j in range(0, 3):
                self.assertAnyMessage()
        self.sc.sendJSON({"commandType": "startGame", "fromId": admin, "gameId": gameId})
        for i in range(0, numberOfPlayers + 3):
            self.assertAnyMessage()
        return gameId

    def clearRecBuffer(self):
        proc = Process(target=clearQueueHelper, args=(self.sc,))
        proc.start()
        time.sleep(1)
        proc.kill()


def clearQueueHelper(sc: ServerConnection):
    while True:
        sc.receiveJSON()


def assertEqual(element1, element2):
    if not element1 == element2:
        raise AssertionError("\nExpected " + str(element1) + "\nBut got " + str(element2))


def assertIn(key, dc):
    if key not in dc:
        raise AssertionError("\nkey " + str(key) + " not found in dict " + str(dc))
