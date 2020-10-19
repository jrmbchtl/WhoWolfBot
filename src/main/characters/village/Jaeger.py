from Types import CharacterType
from Teams import VillagerTeam
from random import randrange


class Jaeger(VillagerTeam):
	def __init__(self, isAlive=True):
		super(self, CharacterType.JAEGER, isAlive)
		self.descriptions = {
			0: """Du bist der Jäger: Sollte er zu Tode kommen, kann er einen letzten Schuss \
			abgeben und einen Mitspieler mit ins Verderben reißen.""",
			1: """Du bist der Jäger, welcher in seinem letzen Atemzug noch zum Gewehr greift, \
			um einen beliebigen Mitspieler ins Jenseits zu befördern.""",
			2: """Bei deinem Charakter handelt es sich um den Jäger, welcher als letzte Aktion \
			vor seinem Tod noch einen Spieler erschießen muss.""",
			3: """Du bist der Jäger. Wenn der Jäger stirbt, muss er noch einen Spieler seiner \
			Wahl in den Tod mitnehmen.""",
			4: """Du bist der Jäger. Scheidet der Jäger aus dem Spiel aus, feuert er in seinem \
			letzten Atemzug noch einen Schuss ab, mit dem er einen Spieler seiner \
			Wahl mit in den Tod reißt.""",
			5: """Du bist der Jäger. Als dieser musst du direkt vor deinem Tod mit deiner Jagdwaffe \
			einen anderen Bewohner des Dorfes erschießen."""
		}

	def getDescription(self):
		return self.descriptions.get(randrange(0, 5))
