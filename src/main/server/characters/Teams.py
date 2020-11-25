from src.main.server.characters.Character import Character
from src.main.server.characters.Types import TeamType


class WerewolfTeam(Character):
	def __init__(self, role, alive):
		super(WerewolfTeam, self).__init__(TeamType.WEREWOLF, role, alive)


class VillagerTeam(Character):
	def __init__(self, role, alive):
		super(VillagerTeam, self).__init__(TeamType.VILLAGER, role, alive)


class WhitewolfTeam(Character):
	def __init__(self, role, alive):
		super(WhitewolfTeam, self).__init__(TeamType.WHITEWOLF, role, alive)
