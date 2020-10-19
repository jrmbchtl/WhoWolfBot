from ..Types import CharacterType, TeamType
from ..Character import Character
import random
from ...Factory import Factory


class Wolfshund(Character):
	def __init__(self, isAlive=True):
		super(self, None, CharacterType.WOLFSHUND, isAlive)
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
		return self.descriptions.get(random.randrange(0, 5))

	def initialWake(self, gameData, playerId):
		intro = Wolfshund.Wolfshund.wolfshundOptions()
		indexWerwolf, optionWerwolf = Wolfshund.wolfshundChooseWerwolf()
		indexDorf, optionDorf = Wolfshund.wolfshundChooseDorf()
		gameData.getServerConnection().sendJSON(
			Factory.createChoiceFieldEvent(playerId, intro, [optionWerwolf, optionDorf]))
		messageId = gameData.getNextMessageDict()["reply"]["messageId"]

		rec = gameData.getNextMessageDict()
		gameData.getServerConnection().sendJSON(
			Factory.createMessageEvent(playerId, intro, messageId, Factory.EditMode.EDIT))
		if rec["reply"]["choiceIndex"] == 0:
			self.setTeam(TeamType.WERWOLF)
			gameData.getServerConnection().sendJSON(
				Factory.createMessageEvent(playerId, Wolfshund.wolfshundDidChooseWerwolf(optionWerwolf)))
		elif rec["reply"]["choiceIndex"] == 1:
			self.setTeam(TeamType.VILLAGER)
			gameData.getServerConnection().sendJSON(
				Factory.createMessageEvent(playerId, Wolfshund.wolfshundDidChooseDorf(optionDorf)))
		else:
			raise ValueError("How can u choose option " + rec["reply"]["choiceIndex"])
		gameData.dumpNextMessageDict()

	def wolfshundOptions():
		desc_no = random.randrange(0, 7)
		if desc_no == 0:
			return "Wie möchtest du dieses Spiel bestreiten?"
		elif desc_no == 1:
			return "Welchem Team möchtest du angehören?"
		elif desc_no == 2:
			return "Welche Gene setzen sich in dir durch?"
		elif desc_no == 3:
			return "Du kommst jetzt in ein Alter, in dem du dich für eine Seite entscheiden mussst."
		elif desc_no == 4:
			return "Wie willst du den Rest deines Lebens verbringen?"
		elif desc_no == 5:
			return "Möchtest du Menschen fressen oder von Menschen gelyncht werden?"
		else:
			return "Es ist an der Zeit, sich für eine Seite zu entscheiden!"

	def wolfshundChooseWerwolf():
		desc_no = random.randrange(0, 7)
		if desc_no == 0:
			return (0, "in einen Werwolf verwandeln")
		elif desc_no == 1:
			return (1, "zum Werwolf mutieren")
		elif desc_no == 2:
			return (2, "das Tier in dir vorkommen lassen")
		elif desc_no == 3:
			return (3, "Blutlust entwickeln")
		elif desc_no == 4:
			return (4, "Hunger auf Menschfleisch bekommen")
		elif desc_no == 5:
			return (5, "dem Dorf den Rücken zuwenden")
		else:
			return (6, "sich den Werwölfen anschließen")

	def wolfshundDidChooseWerwolf(option):
		if option == 0:
			return "Du hast dich in einen Werwolf verwandelt."
		elif option == 1:
			return "Du bist zu einem Werwolf mutiert."
		elif option == 2:
			return "Du hast das Tier in dir durchkommen lassen."
		elif option == 3:
			return "Du hast Blutlust enwickelt."
		elif option == 4:
			return "Du hast Hunger auf Menschfleisch bekommen."
		elif option == 5:
			return "Du hast dem Dorf den Rücken zugewendet."
		else:
			return "Du hast dich den Werwölfen angeschlossen."

	def wolfshundChooseDorf():
		desc_no = random.randrange(0, 7)
		if desc_no == 0:
			return (0, "sich dem Dorf anschließen")
		elif desc_no == 1:
			return (1, "brav im Dorf leben")
		elif desc_no == 2:
			return (2, "harmloser Schoßhund werden")
		elif desc_no == 3:
			return (3, "doch lieber Vegetarier werden")
		elif desc_no == 4:
			return (4, "Wenn du Blut siehst, wird dir schlecht")
		elif desc_no == 5:
			return (5, "Demokratie der Gewalt vorziehen")
		else:
			return (6, "Humanität zeigen")

	def wolfshundDidChooseDorf(option):
		if option == 0:
			return "Du hast dich dem Dorf angeschlossen."
		elif option == 1:
			return "Du lebst von nun an brav im Dorf."
		elif option == 2:
			return "Du bist zu einem harmlosen Schoßhund geworden."
		elif option == 3:
			return "Du hast beschlossen, doch lieber Vegetarier zu werden."
		elif option == 4:
			return "Du hast Hämatophobie."
		elif option == 5:
			return "Du ziehst die Demokratie der Gewalt vor."
		else:
			return "Du zeigst Humanität."
