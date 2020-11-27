from src.main.server.characters.Teams import WerewolfTeam
from src.main.server.characters.Types import CharacterType


class Werewolf(WerewolfTeam):
    def __init__(self, alive=True):
        super(Werewolf, self).__init__(CharacterType.WEREWOLF, "werewolfDescription", alive)
