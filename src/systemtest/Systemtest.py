from src.main.client.conn.ServerConnection import ServerConnection


class Systemtest(object):
    def __init__(self, sc):
        super(Systemtest, self)
        self.sc: ServerConnection = sc

    def run(self):
        pass

    def asserReceiveDict(self, dc):
        rec = self.sc.receiveJSON()
        self.dictCompare(dc, rec)

    def assertAnyMessage(self):
        self.sc.receiveJSON()

    def verifyMessage(self, messageId=112, gameId=1):
        self.sc.sendJSON({"commandType": "feedback", "feedback":
                         {"success": 1, "messageId": messageId}, "gameId": gameId})

    def dictCompare(self, expected, actual):
        for key in expected:
            assertIn(key, actual)
            assertEqual(expected[key], actual[key])
        for key in actual:
            assertIn(key, expected)
            assertEqual(expected[key], actual[key])

    # handles everything including nightfall and returns the gameId
    def initGame(self, numberOfPlayers=4, admin=42):
        self.sc.sendJSON({"commandType": "newGame", "newGame": {"senderId": admin}, "origin": 0})
        gameId = self.sc.receiveJSON()["gameId"]
        self.verifyMessage(0, gameId)
        for i in range(1, numberOfPlayers + 1):
            self.sc.sendJSON({"commandType": "register", "register":
                {"name": "Player " + str(i), "id": i}, "origin": 0, "gameId": gameId})
            for j in range(0, 3):
                self.assertAnyMessage()
                self.verifyMessage()
        self.sc.sendJSON({"commandType": "startGame", "startGame": {"senderId": admin}, "origin": 0,
                          "gameId": gameId})
        for i in range(0, numberOfPlayers + 1):
            self.assertAnyMessage()
            self.verifyMessage()
        return


def assertEqual(element1, element2):
    if not element1 == element2:
        raise AssertionError("\nExpected " + str(element1) + "\nBut got " + str(element2))


def assertIn(key, dc):
    if key not in dc:
        raise AssertionError("\nkey" + str(key) + "not found in dict " + str(dc))
