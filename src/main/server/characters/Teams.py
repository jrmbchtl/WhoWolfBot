from src.main.server.characters.Character import Character
from src.main.server.characters.Types import TeamType


class WerwolfTeam(Character):
	def __init__(self, role, isAlive):
		super(WerwolfTeam, self).__init__(TeamType.WERWOLF, role, isAlive)


class VillagerTeam(Character):
	def __init__(self, role, isAlive):
		super(VillagerTeam, self).__init__(TeamType.VILLAGER, role, isAlive)
