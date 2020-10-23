from src.main.GameData import GameData
from src.main.characters import Types
from src.main.characters.Character import Character


def wake(gameData: GameData):
    werwolfList = []
    for player in gameData.getAlivePlayerList():
        c: Character = gameData.getAlivePlayerList()[player].getCharacter()
        if c.getTeam() == Types.TeamType.WERWOLF:
            werwolfList.append(player)
    text = ""
