class Character(object):

	def __init__(self, team, role, isAlive):
		super(Character, self)
		self.isAlive = isAlive
		self.team = team
		self.role = role

	def isAlive(self):
		return self.isAlive

	def getPriority(self):
		return self.priority

	def getTeam(self):
		return self.team

	def getRole(self):
		return self.role

	def getDescription(self):
		pass

	def kill(self):
		self.isAlive = False

	def wakeUp(self):
		pass
