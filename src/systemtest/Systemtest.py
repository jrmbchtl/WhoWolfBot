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

    def dictCompare(self, expected, actual):
        for key in expected:
            assertIn(key, actual)
            assertEqual(expected[key], actual[key])
        for key in actual:
            assertIn(key, expected)
            assertEqual(expected[key], actual[key])


def assertEqual(element1, element2):
    if not element1 == element2:
        raise AssertionError("\nExpected " + str(element1) + "\nBut got " + str(element2))


def assertIn(key, dc):
    if key not in dc:
        raise AssertionError("\nkey" + str(key) + "not found in dict " + str(dc))
