from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType


class BadassBastard(VillagerTeam):
    def __init__(self, alive=True):
        super(BadassBastard, self).__init__(CharacterType.BADDASSBASTARD, "bbDescription", alive)
        self.secondLive = True

    def hasSecondLive(self):
        return self.secondLive

    def removeSecondLive(self):
        self.secondLive = False
