from src.main.server.characters.Teams import WerwolfTeam
from src.main.server.characters.Types import CharacterType


class Werwolf(WerwolfTeam):
    def __init__(self, isAlive=True):
        super(Werwolf, self).__init__(CharacterType.WERWOLF, isAlive)
        self.descriptions = {
            0: ("Du bist einer der Werwölfe. Diese suchen sich jede Nacht gemeinsam ein Opfer aus, "
                "welches sie töten wollen. Ihr Ziel ist es, dass nur Charaktere der Werwölfe "
                "überleben."),
            1: ("Du bist ein Werwolf. Jede Nacht zieht das Werwolfsrudel umher und sucht sich "
                "gemeinschaftlich ein Opfer aus, dass sie diese Nacht reißen wollen. Die Werwölfe "
                "gewinnen, falls alle Dorfbewohner gestorben sind."),
            2: ("Du gehörst den Werwölfen an. Du suchst dir, zusammen mit den anderen Werwölfen "
                "jede Nacht deinen Mitternachtsimbiss aus."),
            3: ("Du bist ein Werwolf, welcher sich jede Nacht mit seinem Wolfsrudel trifft, "
                "um sich einen Dorfbewohner zum snacken zu 'borgen'."),
            4: ("Du bist ein Werwolf, welcher jede Nacht erwacht und sich ein Opfer unter den "
                "Dorfbewohnern sucht, um dieses dann gemeinsam mit den anderen Werwölfen "
                "anzugreifen."),
            5: ("Du bist ein Werwolf. Da diese Rudeltiere sind, erwachen alle Werwölfe "
                "jede Nacht gemeinsam, um sich ein (hoffentlich) wehrloses Opfer "
                "unter den Dorfbewohnern zu suchen.")
        }

    def getDescription(self, gameData):
        return self.descriptions.get(gameData.randrange(0, 5))
