from conn.ServerConnection import ServerConnection


class Main(object):
	def __init__(self):
		super(Main, self)

	def main(self):
		sc = ServerConnection()
		sc.startServer()

		startGame = {}
		startGame["commandType"] = "newGame"
		startGame["newGame"] = {}
		startGame["origin"] = 1234
		sc.sendJSON(startGame)
		response = sc.receiveJSON()
		print(response)

		sc.closeServer()


if __name__ == "__main__":
	main = Main()
	main.main()
