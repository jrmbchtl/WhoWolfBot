from src.main.server.characters.Character import Character
from src.main.server.characters.Types import TeamType


class WerewolfTeam(Character):
	def __init__(self, role, descString, alive):
		super(WerewolfTeam, self).__init__(TeamType.WEREWOLF, role, descString, alive)


class VillagerTeam(Character):
	def __init__(self, role, descString, alive):
		super(VillagerTeam, self).__init__(TeamType.VILLAGER, role, descString, alive)


class WhitewolfTeam(Character):
	def __init__(self, role, descString, alive):
		super(WhitewolfTeam, self).__init__(TeamType.WHITEWOLF, role, descString, alive)
