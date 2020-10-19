

class GameData(object):
	"""stores data for each game"""
	def __init__(self, gameOver, players, sc, admin, origin, gameQueue, menuMessageId):
		super(GameData, self).__init__()
		self.gameOver = False
		self.players = {}
		self.sc = sc
		self.admin = admin
		self.origin = origin
		self.gameQueue = gameQueue
		self.menuMessageId = None

	def getNextMessageDict(self):
		while self.gameQueue.empty():
			pass
		return self.gameQueue.get()

	def dumpNextMessageDict(self):
		while self.gameQueue.empty():
			pass
		print("Dumped: " + self.gameQueue.get())

	def setGameOver(self, gameOver):
		self.gameOver = gameOver

	def getGameOver(self):
		return self.gameOver

	def setPlayers(self, players):
		self.players = players

	def getPlayers(self):
		return self.players

	def setServerConnection(self, sc):
		self.sc = sc

	def getServerConnection(self):
		return self.sc

	def setAdmin(self, admin):
		self.admin = admin

	def getAdmin(self):
		return self.admin

	def setOrigin(self, origin):
		self.origin = origin

	def getOrigin(self):
		return self.origin

	def setGameQueue(self, gameQueue):
		self.gameQueue = gameQueue

	def getGameQueue(self):
		return self.gameQueue

	def setMenuMessageId(self, menuMessageId):
		self.menuMessageId = menuMessageId

	def getMenuMessageId(self):
		return self.menuMessageId
