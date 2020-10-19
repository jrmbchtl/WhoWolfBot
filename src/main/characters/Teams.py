from Types import TeamType
import Character


class WerwolfTeam(Character):
	def __init__(self, role, isAlive):
		super(WerwolfTeam, self).__init__(TeamType.WERWOLF, role, isAlive)

	def getTeam(self):
		return TeamType.WERWOLF


class VillagerTeam(Character):
	def __init__(self, role, isAlive):
		super(VillagerTeam, self).__init__(TeamType.VILLAGER, role, isAlive)

	def getTeam(self):
		return TeamType.VILLAGER
