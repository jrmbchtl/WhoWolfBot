from Types import CharacterType
from Teams import WerwolfTeam
from random import randrange


class Terrorwolf(WerwolfTeam):
	def __init__(self, isAlive=True):
		super(self, CharacterType.TERRORWOLF, isAlive)
		self.descriptions = {
			0: """Du bist der Terrorwolf. Wenn der Terrorwolf stirbt, nimmt er noch \
			einen Spieler seiner Wahl mit in den Tod.""",
			1: """Du bist der Terrorwolf. Der Terrorwolf ist der Jäger der Werwölfe: \
			Sollte er sterben, kann er noch einen Charakter seiner Wahl mit in den Tod reißen.""",
			2: """Dein Carakter ist der Terrorwolf, welcher, sollte er zu Tode kommen, \
			in letzter Sekunde noch ein Opfer reißen kann.""",
			3: """Du bist der Terrorwolf. Dieser ist ähnlich dem Jäger, mit dem Unterschied, \
			dass er für die Werwölfe spielt: Stirbt der Terrorwolf, egal ob bei Tag oder Nacht, \
			so bleibt ihm noch ausreichend Zeit, sich einen Dorfbewohner als \
			Henkersmahlzeit zu schnappen.""",
			4: """Deine Rolle ist er Terrorwolf, welcher mittels eines Testaments \
			den Tod eines Dorfbewohners einfordert.""",
			5: """Du bist der Terrorwolf. Dein Tod hat Konsequenzen. Zumindest für einen \
			weiteren Dorfbewohner: Wenn du stirbst, steht er als letzte Mahlzeit auf deinem Speiseplan.""",

		}

	def getDescription(self):
		return self.descriptions.get(randrange(0, 5))
