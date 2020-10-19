class Character(object):

	def __init__(self, team, role, isAlive=True):
		super(Character, self)
		self.isAlive = isAlive
		self.role = role
		self.team = None

	def isAlive(self):
		return self.isAlive

	def getPriority(self):
		return self.priority

	def getTeam(self):
		return self.team

	def setTeam(self, team):
		self.team = team

	def getRole(self):
		return self.role

	def setRole(self, role):
		self.role = role

	def getDescription(self):
		pass

	def kill(self):
		self.isAlive = False

	def wakeUp(self, sc):
		pass

	def initialWake(self, gameData):
		pass

	def getCharacterType(self):
		return self.role
