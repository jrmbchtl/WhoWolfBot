from src.main.server import Factory
from src.main.server.characters.Teams import VillagerTeam
from src.main.server.characters.Types import CharacterType


class Hexe(VillagerTeam):
    def __init__(self, isAlive=True):
        super(Hexe, self).__init__(CharacterType.HEXE, isAlive)
        self.descriptions = {
            0: ("Du bist die Hexe. Diese erwacht jede Nacht, erfährt das Opfer der Werwölfe und "
                "darf sich entscheiden, ob sie ihren einen Lebenstrank auf das Opfer anwendet. "
                "Anschließend hat sie die Möglichkeit, einmal im Spiel eine Person mit einem "
                "Todestrank zu ermorden."),
            1: ("Du bist die Hexe. Ihr stehen zwei Tränke zur Verfügung, ein Heil- und ein "
                "Gifttrank. \nDeren Bedeutung ist zwar selbsterklärend, aber dennoch: "
                "Mit dem Gifttrank kann sie einmal im Spiel einen Mitspieler vergiften, "
                "mit dem Heiltrank jemanden vor den Werwölfen erretten (auch sich selber)."),
            2: ("Deine Rolle ist die Hexe. Die Hexe erwacht immer direkt nachdem die Werwölfe ihr "
                "Opfer ausgesucht haben. Sie hat im Verlauf des gesamten Spiels einen Gift- und "
                "einen Heiltrank. Die Hexe erfährt das Mordopfer der Werwölfe und kann dieses mit "
                "ihrem Heiltrank heilen (auch sich selbst), so dass es am nächsten Morgen keinen "
                "Toten gibt. Sie kann aber auch den Gifttrank auf einen anderen Spieler anwenden; "
                "dann gibt es mehrere Tote."),
            3: ("Dein Charakter ist die Hexe. Die Hexe bekommt jede Nacht das Opfer der Werwölfe "
                "angezeigt (sofern jemand durch die Werwölfe sterben würde) und kann einmal im "
                "Spiel das Opfer mit einem Heiltrank retten. Außerdem hat sie einen Todestrank, "
                "mit dem sie einmal im Spiel einen beliebigen Spieler töten kann."),
            4: ("Du bist die Hexe. Ihr stehen im gesamten Spiel zwei verschiedene Tränke zur "
                "Auswahl: Sie darf einmal im Spiel, nachdem sie das Opfer der Werwölfe erfahren "
                "hat, dieses mit dem Lebenstrank retten und einmal im Spiel einen beliebigen "
                "Mitspieler mit einem Gifttrank aus dem Leben schießen."),
            5: ("Bei deiner Rolle handelt es sich um die Hexe. Diese hat zwei Spezialfähigkeiten. "
                "Zum einen darf sie jede Nacht, sofern sie noch ihren einen Heiltrank besitzt, "
                "das Opfer der Werwölfe erfahren und ggf. heilen. Zum anderen darf sie einmal im "
                "Spiel Gift in das Getränk eines Mitspielers geben, welcher dann am nächsten "
                "Morgen nicht mehr erwacht.")
        }
        self.hasLivePotion = True
        self.hasDeathPotion = True

    def getDescription(self, gameData):
        return self.descriptions.get(gameData.randrange(0, 6))

    def wakeUp(self, gameData, playerId):
        if self.hasLivePotion and gameData.getWerwolfTarget() is not None:
            targetName = gameData.getPlayerList()[gameData.getWerwolfTarget()].getName()
            text = targetName + (" wurde diese Nacht von den Werwölfen erwischt. "
                                 "Möchtest du diese Person retten?")
            noSave, optionSave = hexeSave(gameData)
            noLetDie, optionLetDie = hexeLetDie(gameData)
            gameData.sendJSON(Factory.createChoiceFieldEvent(
                playerId, text, [optionSave, optionLetDie]))
            messageId = gameData.getNextMessageDict()["feedback"]["messageId"]

            choice = gameData.getNextMessageDict()["reply"]["choiceIndex"]
            gameData.sendJSON(Factory.createMessageEvent(
                playerId, text, messageId, Factory.EditMode.EDIT))
            gameData.dumpNextMessageDict()
            if choice == 0:
                gameData.setWerwolfTarget(None)
                self.hasLivePotion = False
                gameData.sendJSON(Factory.createMessageEvent(
                    playerId, hexeDidSave(noSave, targetName)))
            elif choice == 1:
                gameData.sendJSON(Factory.createMessageEvent(
                    playerId, hexeDidLetDie(noLetDie, targetName)))
            else:
                raise ValueError("Die Hexe sollte keine Option " + choice + " haben!")
            gameData.dumpNextMessageDict()

        if self.hasDeathPotion:
            text = "Willst du noch jemanden töten?"
            idToNo = {}
            indexToId = {}
            options = []
            index = 0
            for player in gameData.getAlivePlayerList():
                if player != player:
                    no, option = hexeKill(gameData)
                    option = gameData.getAlivePlayers()[player] + option
                    options.append(option)
                    idToNo[player] = no
                    indexToId[index] = player
                    index += 1

            no, option = hexeKill(gameData)
            options.append("Niemanden" + option)

            gameData.sendJSON(Factory.createChoiceFieldEvent(playerId, text, options))
            messageId = gameData.getNextMessageDict()["feedback"]["messageId"]

            choice = gameData.getNextMessageDict()["reply"]["choiceIndex"]
            gameData.sendJSON(Factory.createMessageEvent(
                playerId, text, messageId, Factory.EditMode.EDIT))
            gameData.dumpNextMessageDict()

            if choice == len(gameData.getAlivePlayerList() - 1):
                gameData.setWitchTarget(None)
            else:
                self.hasDeathPotion = False
                gameData.setWitchTarget(indexToId[choice])
                targetName = gameData.getAlivePlayerList()[indexToId[choice]].getName()
                text = hexeDidKill(idToNo[indexToId[choice]], targetName)
                gameData.sendJSON(Factory.createMessageEvent(playerId, text))
                gameData.dumpNextMessageDict()


def hexeSave(gameData):
    switcher = {
        0: "Retten",
        1: "Heilen",
        2: "Einen Lebenstrank verabreichen",
        3: "Erfolgreich die Verletzungen versorgen",
        4: "Wiederbeleben",
        5: "Wieder zusammennähen"
    }
    option = gameData.randrange(0, 6)
    return option, switcher[option]


def hexeLetDie(gameData):
    switcher = {
        0: "Sterben lassen",
        1: "Nicht beachten",
        2: "Dem Schicksal überlassen",
        3: "Ausversehen zu spät kommen",
        4: "Lieber schlafen",
        5: "Umdrehen und weiterschlafen",
        6: "Lebenstrank nicht für sojemanden verschwenden",
        7: "Eigensicherung vorziehen"
    }
    option = gameData.randrange(0, 8)
    return option, switcher[option]


def hexeDidSave(option, name):
    switcher = {
        0: "Du hast " + name + " gerettet.",
        1: "Die Hexe hat " + name + " geheilt.",
        2: "Die Hexe hat " + name + " einen Lebenstrank verabreicht.",
        3: "Du hast " + name + "s Verletzungen erfolgreich versorgt.",
        4: "Die Hexe hat " + name + " wiederbelebt.",
        5: "Die Hexe hat " + name + " wieder zusammengenäht."
    }
    return switcher[option]


def hexeDidLetDie(option, name):
    switcher = {
        0: "Du hast " + name + " sterben gelassen.",
        1: "Die Hexe hat " + name + " nicht beachtet.",
        2: "Die Hexe hat " + name + " dem Schicksal überlassen.",
        3: "Du bist für " + name + " ausversehen zu spät gekommen.",
        4: "Die Hexe hat lieber geschlafen, als " + name + " zu helfen.",
        5: "Die Hexe hat sich einfach umgedreht und weitergeschlafen, als sie von " + name
           + "s Unfall hörte.",
        6: "Die Hexe wollte ihren Lebenstrank nicht für jemanden wie " + name + " verschwenden.",
        7: "Die Hexe hat Eigensicherung vorgezogen statt " + name + " zur Hilfe zu eilen."
    }
    return switcher[option]


def hexeKill(gameData):
    switcher = {
        0: " vergiften",
        1: " den Todestrank einflößen",
        2: " eine ungesunde Substanz injezieren",
        3: " ausversehen eine Überdosis Morphium verabreichen",
        4: " mit radioaktivem Gemüse versorgen",
        5: "s innere Organe verätzen",
        6: " ausversehen Gift in das Getränk mischen",
        7: " ein Essen mit Fliegenpilzen zubereiten",
        8: " einen Kugelfisch falsch zubereiten",
        9: " Quecksilber in die Milch mischen"
    }
    option = gameData.randrange(0, 10)
    return option, switcher[option]


def hexeDidKill(option, name):
    switcher = {
        0: "Du hast " + name + " vergiftet.",
        1: "Die Hexe hat " + name + " den Todestrank eingeflöst.",
        2: "Die Hexe hat " + name + " eine ungesunde Substanz injeziert.",
        3: "Du hast " + name + " eine Überdosis Morphium verabreicht.",
        4: "Die Hexe hat  " + name + " mit radioaktivem Gemüse versorgt.",
        5: "Du hast " + name + "s innere Organe verätzt.",
        6: "Die Hexe hat ausversehen " + name + " Gift ins Getränk gemischt.",
        7: "Die Hexe hat " + name + " ein Essen mit Fliegenpilzen zubereitet.",
        8: "Du hast einen kleinen Fehler gemacht, als du den Kugelfisch für " + name
           + " zubereitet hast.",
        9: "Die Hexe hat " + name + " Quecksilber in die Milch gemischt."
    }
    return switcher[option]
