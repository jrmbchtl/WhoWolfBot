from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType


class Dorfbewohner(VillagerTeam):
    def __init__(self, role=CharacterType.DORFBEWOHNER, isAlive=True):
        super(Dorfbewohner, self).__init__(role, isAlive)
        self.descriptions = {
            0: ("Du bist ein Dorfbewohner, ein normaler Charakter mit keinerlei besonderen "
                "Fähigkeiten."),
            1: ("Bei deiner Rolle handelt es sich um den Dorfbewohner, einem wehrlosen Charakter, "
                "der lediglich tagsüber abstimmen darf."),
            2: ("Du bist ein normaler Dorfbewohner, dessen einzige Waffe die Demokratie am Tage "
                "ist."),
            3: "Dein Charakter ist ein braver Bürger.",
            4: "Du bist ein Dorfbewohner, welcher nachts einfach in Ruhe durchschlafen darf.",
            5: ("Du bist ein normaler Dorfbewohner, welcher sein Überleben nur durch das Lynchen "
                "der Werwölfe am Tage zu schützen weiß.")
        }

    def getDescription(self, gameData):
        return self.descriptions.get(gameData.randrange(0, 5))


class Dorfbewohnerin(Dorfbewohner):
    def __init__(self, isAlive=True):
        super(Dorfbewohnerin, self).__init__(CharacterType.DORFBEWOHNERIN, isAlive)
        self.descriptions = {
            0: ("Du bist eine Dorfbewohnerin, ein normaler Charakter mit keinerlei besonderen "
                "Fähigkeiten."),
            1: ("Bei deiner Rolle handelt es sich um die Dorfbewohnerin, einem wehrlosen "
                "Charakter, der lediglich tagsüber abstimmen darf."),
            2: ("Du bist eine normale Dorfbewohnerin, deren einzige Waffe die Demokratie am "
                "Tage ist."),
            3: "Dein Charakter ist eine brave Bürgerin.",
            4: "Du bist eine Dorfbewohnerin, welche nachts einfach in Ruhe durchschlafen darf.",
            5: ("Du bist eine normale Dorfbewohnerin, welche ihr Überleben nur durch das Lynchen "
                "der Werwölfe am Tage zu schützen weiß.")
        }

    def getDescription(self, gameData):
        return self.descriptions.get(gameData.randrange(0, 5))
