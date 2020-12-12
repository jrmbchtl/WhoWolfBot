"""module for testing game over"""
from src.systemtest.systemtest import Systemtest


class FastDeath(Systemtest):
    """test case aiming for a fast end"""

    def get_name(self):
        return "FastDeath"

    def run(self):
        game_id = self.init_game()

        self.assert_receive_dict({"eventType": "choiceField", "choiceField": {
            "text": "Die Werwolfsmägen knurren vor Hunger - Zeit, sich etwas zu Essen zu suchen!",
            "options": ['Player 1 reißen', 'Player 2 zu Gulasch verarbeiten',
                        'Player 3 durch den Fleischwolf jagen',
                        'Player 4 durch den Fleischwolf jagen',
                        'niemanden die Reißzähne in den Hals rammen'],
            "messageId": 0}, "mode": "write", "target": 3, "highlight": False, "gameId": game_id,
                                  'lang': 'DE'})

        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 3, "gameId": game_id})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": ("Die Werwolfsmägen knurren vor Hunger - Zeit, sich etwas zu Essen zu suchen!"
                     "\n\nPlayer 3 schlägt vor Player 1 zu reißen.\n\n"
                     "Die Werwölfe haben beschlossen, Player 1 zu reißen."),
            "messageId": 24}, "mode": "edit", "target": 3, "highlight": False, "gameId": game_id,
                                  'lang': 'DE'})

        self.assert_receive_dict({"eventType": "choiceField", "choiceField": {
            "text": ("Player 1 wurde diese Nacht von den Werw\u00f6lfen erwischt. M\u00f6chtest "
                     "du diese Person retten?"), "options": [
                         'Retten', 'Ausversehen zu spät kommen'], "messageId": 0},
                                  "mode": "write", "target": 4, "highlight": False,
                                  "gameId": game_id, 'lang': 'DE'})

        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 1},
                        "fromId": 4, "gameId": game_id})
        self.assert_receive_dict({"eventType": "message", "message": {
            "text": ("Player 1 wurde diese Nacht von den Werw\u00f6lfen erwischt. M\u00f6chtest "
                     "du diese Person retten?"), "messageId": 26}, "mode": "edit", "target": 4,
                                  "highlight": False, "gameId": game_id, 'lang': 'DE'})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": "Du bist für Player 1 ausversehen zu spät gekommen.",
            "messageId": 0}, "mode": "write", "target": 4,
                                  "highlight": False, "gameId": game_id, 'lang': 'DE'})

        self.assert_receive_dict({"eventType": "choiceField", "choiceField": {
            "text": "Willst du noch jemanden t\u00f6ten?",
            "options": ['Player 1 einen Kugelfisch falsch zubereiten',
                        'Player 2 ausversehen Gift in das Getränk mischen',
                        'Player 3 ausversehen eine Überdosis Morphium verabreichen',
                        'Niemanden ein Essen mit Fliegenpilzen zubereiten'],
            "messageId": 0}, "mode": "write", "target": 4, "highlight": False, "gameId": game_id,
                                  'lang': 'DE'})

        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 2},
                        "fromId": 4, "gameId": game_id})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": ("Willst du noch jemanden t\u00f6ten?\n\nDu hast Player 3 eine Überdosis "
                     "Morphium verabreicht."), "messageId": 29},
                                  "mode": "edit", "target": 4, "highlight": False,
                                  "gameId": game_id, 'lang': 'DE'})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": "Player 1 besucht nun die ewigen Jagdgründe.", "messageId": 0},
                                  "mode": "write", "target": 0, "highlight": True,
                                  "gameId": game_id, 'lang': 'DE'})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": "Player 1 besucht nun die ewigen Jagdgründe.", "messageId": 0},
                                  "mode": "write", "target": 1, "highlight": True,
                                  "gameId": game_id, 'lang': 'DE'})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": ("Player 1 versucht mit Waffengewalt, kurz vor seinem Tod noch für "
                     "Gerechtigkeit zu sorgen!"), "messageId": 0},
                                  "mode": "write", "target": 0, "highlight": False,
                                  "gameId": game_id, 'lang': 'DE'})

        self.assert_receive_dict({"eventType": "choiceField", "choiceField": {
            "text": "Wen möchtest du mit ins Grab nehmen?", "options":
                ['Player 2 durchlöchern', 'Player 4 niederstrecken'],
            "messageId": 0}, "mode": "write", "target": 1, "highlight": False, "gameId": game_id,
                                  'lang': 'DE'})

        self.send_json({"commandType": "reply", "reply": {"choiceIndex": 0},
                        "fromId": 1, "gameId": game_id})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": "Wen möchtest du mit ins Grab nehmen?", "messageId": 34},
                                  "mode": "edit", "target": 1, "highlight": False,
                                  "gameId": game_id, 'lang': 'DE'})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": "Player 2 hat nun sehr viele Löcher in Kopf und Brust.", "messageId": 0},
                                  "mode": "write", "target": 0, "highlight": True,
                                  "gameId": game_id, 'lang': 'DE'})
        self.assert_receive_dict({"eventType": "message", "message": {
            "text": "Player 2 hat nun sehr viele Löcher in Kopf und Brust.", "messageId": 0},
                                  "mode": "write", "target": 2, "highlight": True,
                                  "gameId": game_id, 'lang': 'DE'})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": "Player 3 ist nicht mehr aufzufinden.", "messageId": 0},
                                  "mode": "write", "target": 0, "highlight": True,
                                  "gameId": game_id, 'lang': 'DE'})
        self.assert_receive_dict({"eventType": "message", "message": {
            "text": "Player 3 ist nicht mehr aufzufinden.", "messageId": 0},
                                  "mode": "write", "target": 3, "highlight": True,
                                  "gameId": game_id, 'lang': 'DE'})

        self.assert_receive_dict({"eventType": "message", "message": {
            "text": ("Es wird wieder friedlich in Düsterwald, da hier nur noch Dorfbewohner "
                     "leben."), "messageId": 0},
                                  "mode": "write", "target": 0, "highlight": True,
                                  "gameId": game_id, 'lang': 'DE'})

        self.send_json({"commandType": "terminate", "fromId": 42, "gameId": game_id})
        self.clear_rec_buffer()
