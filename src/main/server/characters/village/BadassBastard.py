from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc


class BadassBastard(VillagerTeam):
    def __init__(self, alive=True):
        super(BadassBastard, self).__init__(CharacterType.BADDASSBASTARD, alive)
        self.secondLive = True

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "bbDescription")
        return dc[str(gameData.randrange(0, len(dc)))]

    def hasSecondLive(self):
        return self.secondLive

    def removeSecondLive(self):
        self.secondLive = False
