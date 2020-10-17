from enum import Enum
from Player import Player


class State(Enum):
	REGISTER = 0,
	NIGHT = 1,
	ACCUSE = 2,
	VOTE = 3,
	GAMEEND = 10


class Server(object):
	def __init__(self, sc, admin, origin):
		super(Server, self)
		self.gameOver = False
		self.players = {}
		self.sc = sc
		self.admin = admin
		self.origin = origin

	def start(self):
		self.state = State.REGISTER
		self.register()
		while(not self.state != State.GAMEEND):
			self.state = State.NIGHT
			self.night()
			if (self.state == State.GAMEEND):
				break
			self.state = State.ACCUSE
			self.accuse()
			self.state = State.VOTE
			self.vote()

	def register(self):
		rec = self.sc.receiveJSON()
		while rec["commandType"] != "startGame" and rec["startGame"]["senderId"] != self.admin:
			if rec["commandType"] == "register":
				if rec["register"]["id"] not in self.players:
					player = Player(rec["register"]["name"])
					self.players[rec["register"]["id"]] = player
				else:
					self.players.pop(rec["register"]["id"], None)
				self.sendCurrentPlayerList()

	def sendCurrentPlayerList(self):
		pass

	def night(self):
		pass

	def accuse(self):
		pass

	def vote(self):
		pass
