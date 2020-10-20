from .Types import TeamType
from .Character import Character


class WerwolfTeam(Character):
	def __init__(self, role, isAlive):
		super(WerwolfTeam, self).__init__(TeamType.WERWOLF, role, isAlive)


class VillagerTeam(Character):
	def __init__(self, role, isAlive):
		super(VillagerTeam, self).__init__(TeamType.VILLAGER, role, isAlive)
