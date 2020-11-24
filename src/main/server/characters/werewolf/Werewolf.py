from src.main.server.characters.Teams import WerewolfTeam
from src.main.server.characters.Types import CharacterType
from src.main.localization import getLocalization as loc


class Werewolf(WerewolfTeam):
    def __init__(self, alive=True):
        super(Werewolf, self).__init__(CharacterType.WEREWOLF, alive)

    def getDescription(self, gameData):
        dc = loc(gameData.getLang(), "werewolfDescription")
        return dc[str(gameData.randrange(0, len(dc)))]
