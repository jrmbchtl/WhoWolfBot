from ..Types import CharacterType
from ..Teams import VillagerTeam


class Hexe(VillagerTeam):
	def __init__(self, isAlive=True):
		super(Hexe, self).__init__(CharacterType.HEXE, isAlive)
		self.descriptions = {
			0: """Du bist die Hexe. Diese erwacht jede Nacht, erfährt das Opfer der Werwölfe und darf sich \
			entscheiden, ob sie ihren einen Lebenstrank auf das Opfer anwendet. Anschließend hat sie die \
			Möglichkeit, einmal im Spiel eine Person mit einem Todestrank zu ermorden.""",
			1: """Du bist die Hexe. Ihr stehen zwei Tränke zur Verfügung, ein Heil- und ein Gifttrank. \n\
			Deren Bedeutung ist zwar selbsterklärend, aber dennoch: \
			Mit dem Gifttrank kann sie einmal im Spiel einen Mitspieler vergiften, \
			mit dem Heiltrank jemanden vor den Werwölfen erretten (auch sich selber).""",
			2: """Deine Rolle ist die Hexe. Die Hexe erwacht immer direkt nachdem die Werwölfe ihr Opfer \
			ausgesucht haben. Sie hat im Verlauf des gesamten Spiels einen Gift- und einen Heiltrank. \
			Die Hexe erfährt das Mordopfer der Werwölfe und kann dieses mit ihrem Heiltrank heilen \
			(auch sich selbst), so dass es am nächsten Morgen keinen Toten gibt. Sie kann aber auch \
			den Gifttrank auf einen anderen Spieler anwenden; dann gibt es mehrere Tote.""",
			3: """Dein Charakter ist die Hexe. Die Hexe bekommt jede Nacht das Opfer der Werwölfe angezeigt \
			(sofern jemand durch die Werwölfe sterben würde) und kann einmal im Spiel das Opfer \
			mit einem Heiltrank retten. Außerdem hat sie einen Todestrank, mit dem sie einmal im Spiel \
			einen beliebigen Spieler töten kann.""",
			4: """Du bist die Hexe. Ihr stehen im gesamten Spiel zwei verschiedene Tränke zur Auswahl: \
			Sie darf einmal im Spiel, nachdem sie das Opfer der Werwölfe erfahren hat, dieses mit dem \
			Lebenstrank retten und einmal im Spiel einen beliebigen Mitspieler \
			mit einem Gifttrank aus dem Leben schießen.""",
			5: "Bei deiner Rolle handelt es sich um die Hexe. Diese hat zwei Spezialfähigkeiten. \
			Zum einen darf sie jede Nacht, sofern sie noch ihren einen Heiltrank besitzt, \
			das Opfer der Werwölfe erfahren und ggf. heilen. Zum anderen darf sie einmal im Spiel Gift \
			in das Getränk eines Mitspielers geben, welcher dann am nächsten Morgen nicht mehr erwacht."""
		}

	def getDescription(self, gameData):
		return self.descriptions.get(gameData.randrange(0, 6))

	def wakeUp(self, gameData, playerId):
		pass
