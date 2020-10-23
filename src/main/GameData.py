import random


class GameData(object):
	"""stores data for each game"""
	def __init__(self, seed, gameOver, players, sc, admin, origin, gameQueue, gameId, menuMessageId):
		super(GameData, self).__init__()
		random.seed(seed)
		self.gameOver = gameOver
		self.players = players
		self.sc = sc
		self.admin = admin
		self.origin = origin
		self.gameQueue = gameQueue
		self.gameId = gameId
		self.menuMessageId = menuMessageId

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

	def getPlayerList(self):
		return self.getPlayers().keys()

	def getAlivePlayers(self):
		alivePlayers = {}
		for player in self.players:
			if self.players[player].isAlive():
				alivePlayers[player] = self.players[player]
		return alivePlayers

	def getAlivePlayerList(self):
		return self.getAlivePlayers().keys()

	def sendJSON(self, dc):
		dc["gameId"] = self.gameId
		self.sc.sendJSON()

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

	def randrange(self, start, stop, step=1):
		return random.randrange(start, stop, step)

	def random(self):
		return random.random()

	def shuffle(self, ls):
		random.shuffle(ls)
