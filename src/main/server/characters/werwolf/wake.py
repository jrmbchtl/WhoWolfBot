from src.main.server.GameData import GameData
from src.main.server.characters import Types
from src.main.server.characters.Character import Character


def wake(gameData: GameData):
    werwolfList = []
    for player in gameData.getAlivePlayerList():
        c: Character = gameData.getAlivePlayerList()[player].getCharacter()
        if c.getTeam() == Types.TeamType.WERWOLF:
            werwolfList.append(player)
    text = ""
