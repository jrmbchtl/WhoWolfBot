from Types import CharacterType
from Teams import WerwolfTeam
from random import randrange


class Wolfshund(WerwolfTeam):
	def __init__(self, isAlive=True):
		super(self, CharacterType.WOLFSHUND, isAlive)
		self.descriptions = {
			0: """Du bist der Wolfshund. Als dieser darfst du in der ersten Nacht entscheiden, \
			ob du das Spiel als Werwolf oder als Dorfbewohner spielen willst.""",
			1: """Du bist ein Wolfshund, welcher sowohl die Gene eines friedlichen Hundes \
			als auch die eines Wolfes in sich hat. Er entscheidet sich in der ersten Nacht, \
			ob er zum Dorf oder zu den Werwölfen gehören will.""",
			2: """Deine Rolle ist der Wolfshund. Der Wolfshund entscheidet sich in der ersten \
			Nacht, ob er zu den Dorfbewohnern oder zu den Werwölfen gehören will.""",
			3: """Dein Charakter ist der Wolfshund, welcher in der ersten Nacht vor den \
			Werwölfen erwacht und sich entscheiden muss, ob er zu den Werwölfen oder zum Dorf gehört.""",
			4: """Du bist der Wolfshund. Der Wolfshund hat die Wahl, ob er das Spiel als Werwolf \
			oder Dorfbewohner bestreiten will.""",
			5: """Du bist der Wolfshund und besitzt die Fähigkeit, dich zu Beginn des Spieles \
			zu entscheiden, ob du ein Dorfbewohner oder ein Werwolf wirst.""",
		}

	def getDescription(self):
		return self.descriptions.get(randrange(0, 5))
