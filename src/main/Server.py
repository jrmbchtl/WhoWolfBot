from enum import Enum
import random
from Player import Player
from characters.Types import CharacterType
from characters.vilage.Dorfbewohner import Dorfbewohner, Dorfbewohnerin
from characters.vilage.Hexe import Hexe
from characters.vilage.Jaeger import Jaeger
from characters.vilage.Seherin import Seherin
from characters.werwolf.Werwolf import Werwolf
from characters.werwolf.Wolfshund import Wolfshund
from characters.werwolf.Terrorwolf import Terrorwolf
import Factory


class State(Enum):
	REGISTER = 0,
	NIGHT = 1,
	ACCUSE = 2,
	VOTE = 3,
	GAMEEND = 10


class Server(object):
	def __init__(self, sc, admin, origin, gameQueue):
		super(Server, self)
		self.gameOver = False
		self.players = {}
		self.sc = sc
		self.admin = admin
		self.origin = origin
		self.gameQueue = gameQueue
		self.menuMessageId = None

	def start(self):
		self.state = State.REGISTER
		self.register()
		self.rollRoles()
		while(not self.state != State.GAMEEND):
			self.state = State.NIGHT
			self.night()
			if (self.state == State.GAMEEND):
				break
			self.state = State.ACCUSE
			self.accuse()
			self.state = State.VOTE
			self.vote()

	def getNextMessageDict(self):
		while self.gameQueue.empty():
			pass
		return self.gameQueue.get()

	def dumpNextMessageDict(self):
		while self.gameQueue.empty():
			pass
		print("Dumped: " + self.gameQueue.get())

	def updateRegisterMenu(self):
		message = """Viel Spass beim Werwolf spielen!\n\nBitte einen privaten Chat mit dem Bot starten, \
		bevor das Spiel beginnt!\n\nUm das Spiel in seiner vollen Breite genießen zu können, \
		empfiehlt es sich bei sehr schmalen Bildschirmen, diese quer zu verwenden.\n\n"""
		message += "Spieler:\n"
		for player in self.players:
			message += player.getName() + "\n"
		options = ["Mitspielen/Aussteigen", "Start", "Cancel"]
		sendDict = {}
		if self.menuMessageId is None:
			sendDict = Factory.createChoiceField(self.origin, message, options)
		else:
			sendDict = Factory.createChoiceField(self.origin,
				message, options, self.menuMessageId, Factory.EditMode.EDIT)
		self.sc.sendJSON(sendDict)

		rec = self.getNextMessageDict()
		self.menuMessageId = rec["feedback"]["messageId"]

	def register(self):
		rec = self.getNextMessageDict()
		while (rec["commandType"] != "startGame" or rec["startGame"]["senderId"] != self.admin
			or self.players.len() < 4):
			if rec["commandType"] == "register":
				if rec["register"]["id"] not in self.players:
					Factory.createMessage(rec["register"]["id"], "Ich bin der Werwolfbot")
					tmp = self.getNextMessageDict()
					if tmp["feedback"]["success"] == 0:
						self.sc.sendJSON(Factory.createMessage(self.origin,
							"@" + rec["register"]["name"] + ", bitte öffne einen privaten Chat mit mir"))
						self.dumpNextMessageDict()
						continue
					else:
						player = Player(rec["register"]["name"])
						self.players[rec["register"]["id"]] = player
				else:
					self.players.pop(rec["register"]["id"], None)
				self.updateRegisterMenu()
				rec = self.getNextMessageDict()

	def getPlayerList(self):
		return self.players.keys()

	def removeCharacterTypeFromList(self, ls, ct):
		i = 0
		while i < ls.len():
			if ls[i].getCharacterType() == ct:
				del ls[i]
			else:
				i += 1

	def getWerwolfRoleList(self, amountOfPlayers):
		werwolfRoleList = []
		if amountOfPlayers >= 6:
			for i in range(0, 20):
				werwolfRoleList.append(Werwolf())
			for i in range(0, 40):
				werwolfRoleList.append(Wolfshund())
		else:
			for i in range(0, 60):
				werwolfRoleList.append(Werwolf())
		for i in range(0, 40):
			werwolfRoleList.append(Terrorwolf())
		return werwolfRoleList

	def getVillagerRoleList(self):
		dorfRoleList = []
		for i in range(0, 30):
			dorfRoleList.append(Dorfbewohner())
			dorfRoleList.append(Dorfbewohnerin())
		for i in range(0, 28):
			dorfRoleList.append(Jaeger())
		for i in range(0, 28):
			dorfRoleList.append(Seherin())
		for i in range(0, 28):
			dorfRoleList.append(Hexe())
		return dorfRoleList

	def rollRoles(self):
		playerList = self.gtePlayerList()
		random.shuffle(playerList)

		werwolfRoleList = self.getWerwolfRoleList(len(playerList))
		dorfRoleList = self.getVillagerRoleList()

		unique = [CharacterType.JAEGER, CharacterType.SEHERIN, CharacterType.HEXE,
		CharacterType.WOLFSHUND, CharacterType.TERROWOLF]

		group_mod = random.random() * 0.2 + 0.9
		werwolf_amount = int(round(len(playerList) * (1.0 / 3.5) * group_mod, 0))
		for i, p in enumerate(playerList):
			if i < werwolf_amount:
				role = random.randrange(0, len(werwolfRoleList))
				self.players[p].setCharacter(role)
				if role.getCharacterType() in unique:
					self.removeCharacterTypeFromList(werwolfRoleList, role.getCharacterType())
			else:
				role = random.randrange(0, len(dorfRoleList))
				self.players[p].setCharacter(role)
				if role.getCharacterType() in unique:
					self.emoveCharacterTypeFromList(dorfRoleList, role.getCharacterType())
			self.sc.sendJSON(Factory.createMessageEvent(p, self.players[p].getDescription()))
			self.dumpNextMessageDict()

	def night(self):
		pass

	def accuse(self):
		pass

	def vote(self):
		pass
