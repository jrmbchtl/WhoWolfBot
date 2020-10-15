from Types import CharacterType
from Teams import VillagerTeam


class Dorfbewohner(VillagerTeam):
	def __init__(self, role=CharacterType.DORFBEWOHNER, isAlive=True):
		super(Dorfbewohner, self).__init__(role, isAlive)
