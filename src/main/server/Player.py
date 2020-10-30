

class Player(object):
	def __init__(self, name):
		super(Player, self)
		self.name = name
		self.character = None

	def getName(self):
		return self.name

	def getCharacter(self):
		return self.character

	def setCharacter(self, character):
		self.character = character
