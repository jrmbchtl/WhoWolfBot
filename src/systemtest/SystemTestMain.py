import socket
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
        SystemTestRegistration(self).register()
        if not serverIsRunning():
            print("Server is not running, starting it")
            self.server = Process(target=launchServer)
            self.server.start()
            time.sleep(5)
        else:
            print("Server was already started, using running instance")
        self.serverConnection.startServer()
        for test in self.tests:
            print("\n\n##########################################################################")
            print("Running test " + test.getName() + "\n\n")
            test.run()
            print("\n\n")

        self.server.kill()
        self.serverConnection.closeServer()

    def register(self, test):
        self.tests.append(test)

    def getSc(self):
        return self.serverConnection


def serverIsRunning():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 32000))
    if result == 0:
        isOpen = True
    else:
        isOpen = False
    sock.close()
    return isOpen


def launchServer():
    Main().main()


if __name__ == "__main__":
    main = SystemTestMain()
    main.main()
