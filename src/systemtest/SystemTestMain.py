import json
import os
import time

from multiprocessing import Process
from src.main.client.conn.ServerConnection import ServerConnection
from src.main.server.Main import Main
from src.systemtest.SystemTestRegistration import SystemTestRegistration


class SystemTestMain(object):
    def __init__(self):
        super(SystemTestMain, self)
        self.tests = []
        self.serverConnection = ServerConnection()
        self.server = None

    def main(self):
        self.cleanUp()
        SystemTestRegistration(self).register()
        self.server = Process(target=launchServer)
        self.server.start()
        time.sleep(5)
        self.serverConnection.startServer()
        for test in self.tests:
            print("\n\n##########################################################################")
            print("Running test " + test.getName() + "\n\n")
            test.run()
            time.sleep(5)
            print("\n\n")
        self.cleanUp()
        self.server.kill()
        self.serverConnection.closeServer()

    def register(self, test):
        self.tests.append(test)

    def getSc(self):
        return self.serverConnection

    def cleanUp(self):
        files = os.listdir("games/")
        for f in files:
            if os.path.isfile("games/" + f) and f.endswith(".game"):
                with open("games/" + f, "r") as file:
                    data = json.load(file)
                    if data["seed"] != 16384:
                        os.remove("games/" + f)


def launchServer():
    Main().main()


if __name__ == "__main__":
    main = SystemTestMain()
    main.main()
