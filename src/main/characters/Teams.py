from Types import TeamType
from Character import Character


class WerwolfTeam(Character):
	def __init__(self, role, isAlive):
		super(self, TeamType.WERWOLF, role, isAlive)


class VillagerTeam(Character):
	def __init__(self, role, isAlive):
		super(self, TeamType.VILLAGER, role, isAlive)
