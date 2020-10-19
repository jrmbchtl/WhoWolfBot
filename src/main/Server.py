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
from Factory import Factory
from GameData import GameData


class Server(object):
	def __init__(self, sc, admin, origin, gameQueue):
		super(Server, self)
		self.gameData = GameData(gameOver=False, players={}, sc=sc, admin=admin,
			origin=origin, gameQueue=gameQueue, menuMessagId=None)

	def start(self):
		self.register()
		self.rollRoles()
		while(not self.gameData.getGameOver()):
			self.night()
			if (self.gameData.getGameOver()):
				break
			self.accuse()
			self.vote()

	def updateRegisterMenu(self):
		message = """Viel Spass beim Werwolf spielen!\n\nBitte einen privaten Chat mit dem Bot starten, \
		bevor das Spiel beginnt!\n\nUm das Spiel in seiner vollen Breite genießen zu können, \
		empfiehlt es sich bei sehr schmalen Bildschirmen, diese quer zu verwenden.\n\n"""
		message += "Spieler:\n"
		for player in self.gameData.getPlayers():
			message += player.getName() + "\n"
		options = ["Mitspielen/Aussteigen", "Start", "Cancel"]
		sendDict = {}
		if self.gameData.getMenuMessageId() is None:
			sendDict = Factory.createChoiceField(self.gameData.getOrigin(), message, options)
		else:
			sendDict = Factory.createChoiceField(self.gameData.getOrigin(),
				message, options, self.gameData.getMenuMessageId(), Factory.EditMode.EDIT)
		self.gameData.getServerConnection.sendJSON(sendDict)

		rec = self.gameData.getNextMessageDict()
		self.gameData.setMenuMessageId(rec["feedback"]["messageId"])

	def register(self):
		rec = self.gameData.getNextMessageDict()
		while (rec["commandType"] != "startGame"
			or rec["startGame"]["senderId"] != self.gameData.getAdmin()
			or self.gameData.getPlayers().len() < 4):
			if rec["commandType"] == "register":
				if rec["register"]["id"] not in self.gameData.getPlayers():
					Factory.createMessage(rec["register"]["id"], "Ich bin der Werwolfbot")
					tmp = self.gameData.getNextMessageDict()
					if tmp["feedback"]["success"] == 0:
						self.sc.sendJSON(Factory.createMessage(self.gameData.getOrigin(),
							"@" + rec["register"]["name"] + ", bitte öffne einen privaten Chat mit mir"))
						self.gameData.dumpNextMessageDict()
						continue
					else:
						player = Player(rec["register"]["name"])
						self.gameData.getPlayers()[rec["register"]["id"]] = player
				else:
					self.gameData.getPlayers().pop(rec["register"]["id"], None)
				self.updateRegisterMenu()
				rec = self.gameData.getNextMessageDict()

	def getPlayerList(self):
		return self.gameData.getPlayers().keys()

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
		playerList = self.getPlayerList()
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
				self.gameData.getPlayers()[p].setCharacter(role)
				if role.getCharacterType() in unique:
					self.removeCharacterTypeFromList(werwolfRoleList, role.getCharacterType())
			else:
				role = random.randrange(0, len(dorfRoleList))
				self.gameData.getPlayers()[p].setCharacter(role)
				if role.getCharacterType() in unique:
					self.removeCharacterTypeFromList(dorfRoleList, role.getCharacterType())
			self.gameData.getServerConnection().sendJSON(
				Factory.createMessageEvent(p, self.gameData.getPlayers()[p].getDescription()))
			self.gameData.dumpNextMessageDict()

	def night(self):
		pass

	def accuse(self):
		pass

	def vote(self):
		pass
