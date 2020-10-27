from src.main.server.characters.Character import Character
from src.main.server.characters.Types import TeamType


class WerwolfTeam(Character):
	def __init__(self, role, alive):
		super(WerwolfTeam, self).__init__(TeamType.WERWOLF, role, alive)


class VillagerTeam(Character):
	def __init__(self, role, alive):
		super(VillagerTeam, self).__init__(TeamType.VILLAGER, role, alive)
