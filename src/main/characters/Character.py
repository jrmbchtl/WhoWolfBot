class Character(object):

	def __init__(self, role, isAlive=True):
		super(Character, self)
		self.isAlive = isAlive
		self.role = role

	def isAlive(self):
		return self.isAlive

	def getPriority(self):
		return self.priority

	def getTeam(self):
		return self.team

	def getRole(self):
		return self.role.getTeam

	def getDescription(self):
		pass

	def kill(self):
		self.isAlive = False

	def wakeUp(self):
		pass

	def getCharacterType(self):
		return self.role
