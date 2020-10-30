from src.main.client.Client import Client
from src.main.client.conn.ServerConnection import ServerConnection


class Main(object):
	def __init__(self):
		super(Main, self)

	def main(self):
		sc = ServerConnection()
		sc.startServer()

		client = Client(sc)
		client.run()

		sc.closeServer()


if __name__ == "__main__":
	main = Main()
	main.main()
