from Types import CharacterType
from Teams import VillagerTeam
from random import randrange


class Seherin(VillagerTeam):
	def __init__(self, isAlive=True):
		super(self, CharacterType.SEHERIN, isAlive)
		self.descriptions = {
			0: """Du bist die Seherin. Diese erwacht jede Nacht, sucht sich einen Bewohner \
			aus und erfährt, ob dieser zu den Werwölfen gehört oder nicht.""",
			1: """Du bist die Seherin. Die Seherin hat die Fähigkeit, jede Nacht über einen \
			Mitspieler zu erfahren, ob dieser zu den Werwölfen gehört.""",
			2: """Bei deinem Charakter handelt es sich um die Seherin. Jede Nacht erhält sie \
			Einsicht über einen Spieler, ob dieser zu den Werwölfen gehört.""",
			3: """Du bist die Seherin. Die Seherin erwählt jede Nacht einen Spieler. Sie erfährt, \
			ob dieser gut oder böse ist.""",
			4: """Du bist die Seherin. Die Seherin erwacht, während alle anderen schlafen und darf \
			sich eine Person aussuchen, über die sie erfahren will, ob diese gut oder böse ist. \
			Da die Seherin zu jeder Runde die Gruppenzugehörigkeit einer weiteren Person \
			im Spiel kennt, kann sie großen Einfluss nehmen, muss aber ihr Wissen vorsichtig einsetzen.""",
			5: """Dein Charakter ist die Seherin. Als diese erhälst du die Fähigkeit, \
			jede Nacht über eine ander Person zu erfahren, ob diese gut oder böse ist."""
		}

	def getDescription(self):
		return self.descriptions.get(randrange(0, 5))

	def wakeUp(self):
		pass
