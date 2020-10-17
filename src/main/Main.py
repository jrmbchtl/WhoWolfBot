from conn.ServerConnection import ServerConnection
from Server import Server
import threading


class Main(object):
	def __init__(self):
		super(Main, self)
		self.nextFreePort = 16384

	def main(self):
		sc = ServerConnection(self.nextFreePort)
		self.nextFreePort += 1
		sc.startServer()
		try:
			while True:
				dc = sc.receiveJSON()
				if ("commandType" in dc and dc["commandType"] == "newGame"):
					threading.Thread(target=startNewGame, args=(sc, dc, self.nextFreePort, )).start()
		except KeyboardInterrupt:
			pass
		sc.closeServer()


def startNewGame(sc, dc, nextFreePort):
	response = {}
	response["eventType"] = "acceptNewGame"
	acceptNewGame = {}
	acceptNewGame["gameId"] = nextFreePort
	acceptNewGame["port"] = nextFreePort
	response["acceptNewGame"] = acceptNewGame
	response["target"] = dc["origin"]
	sc.sendJSON(response)
	serverConnection = ServerConnection(nextFreePort)
	server = Server(serverConnection, dc["newGame"]["senderId"], dc["origin"])
	server.start()


if __name__ == "__main__":
	main = Main()
	main.main()
