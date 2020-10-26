import socket
import threading

from src.main.client.conn.ServerConnection import ServerConnection
from src.main.server.Main import Main
from src.systemtest.SystemTestRegistration import SystemTestRegistration


class SystemTestMain(object):
    def __init__(self):
        super(SystemTestMain, self)
        self.tests = []
        self.serverConnection = ServerConnection()
        self.serverConnection.startServer()

    def main(self):
        SystemTestRegistration(self).register()
        if not serverIsRunning():
            print("Server is not running, starting it")
            threading.Thread(target=launchServer).start()
        else:
            print("Server was already started, using running instance")
        for test in self.tests:
            test.run()

        self.serverConnection.closeServer()

    def register(self, test):
        self.tests.append(test)


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
    Main.main()


if __name__ == "__main__":
    main = SystemTestMain()
    main.main()
