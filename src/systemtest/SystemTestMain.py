import json
import os
import time

from src.main.client.conn.ServerConnection import ServerConnection
from src.systemtest.SystemTestRegistration import SystemTestRegistration


class SystemTestMain(object):
    def __init__(self, recQueue, sendQueue):
        super(SystemTestMain, self)
        self.tests = []
        self.serverConnection = ServerConnection(recQueue, sendQueue)

    def main(self):
        self.cleanUp()
        SystemTestRegistration(self).register()
        for test in self.tests:
            print("\n\n##########################################################################")
            print("Running test " + test.getName() + "\n\n")
            test.run()
            print("\n\n")
        time.sleep(5)
        self.cleanUp()
        self.serverConnection.sendJSON({"commandType": "close"})

    def register(self, test):
        self.tests.append(test)

    def getSc(self):
        return self.serverConnection

    def cleanUp(self):
        if not os.path.isdir("games"):
            return
        files = os.listdir("games/")
        for f in files:
            if os.path.isfile("games/" + f) and f.endswith(".game"):
                with open("games/" + f, "r") as file:
                    os.system("cat games/" + f)
                    data = json.load(file)
                    if data["seed"] != 16384:
                        os.remove("games/" + f)
