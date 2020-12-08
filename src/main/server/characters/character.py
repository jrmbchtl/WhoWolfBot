"""module for an abstract character"""
from src.main.localization import get_localization as loc
from src.main.server import factory
from src.main.server.utils import Utils


class Character:
    """abstarct class for all characters"""

    def __init__(self, team, role, desc_string, alive=True):
        super()
        self.alive = alive
        self.role = role
        self.team = team
        self.beloved = None
        self.desc_string = desc_string

    def is_alive(self):
        """returns if character is alive"""
        return self.alive

    def get_team(self):
        """returns team of character"""
        return self.team

    def set_team(self, team):
        """sets the team"""
        self.team = team

    def get_role(self):
        """returns the role"""
        return self.role

    def get_description(self, game_data):
        """returns the description of the character"""
        dic = loc(game_data.get_lang(), self.desc_string)
        return dic[str(Utils.randrange(0, len(dic)))]

    def get_beloved(self):
        """returns the beloved of that character"""
        return self.beloved

    def set_beloved(self, beloved):
        """sets the characters loved one"""
        self.beloved = beloved

    def werewolf_kill_attempt(self):
        """for badass bastard"""
        return self.role is not None

    def has_second_live(self):
        """for berserk"""
        return self.role is None

    def kill(self, game_data, player_id, death_message=None):
        """kill the character"""
        self.alive = False
        if death_message is None:
            death_message = game_data.get_players()[player_id].get_name() + game_data.get_message(
                "deathMessage", config={"rndm": True})
        game_data.send_json(
            factory.create_message_event(game_data.get_origin(), death_message,
                                         config={"highlight": True}))
        game_data.dump_next_message(command_type="feedback")
        game_data.send_json(factory.create_message_event(player_id, death_message,
                                                         config={"highlight": True}))
        game_data.dump_next_message(command_type="feedback")
        if self.beloved is not None and self.beloved in game_data.get_alive_players():
            beloved_name = game_data.get_alive_players()[self.beloved].get_name()
            love_dm = beloved_name + game_data.get_message("lovedOneKilled", config={"rndm": True})
            game_data.get_alive_players()[self.beloved].get_character() \
                .kill(game_data, self.beloved, love_dm)

    def wake_up(self, game_data, player_id):
        """wakes up character"""

    def get_character_type(self):
        """gets the role of the character"""
        return self.role

    def can_be_killed(self, game_data):
        """check for redhat"""
        return self.role is not None and game_data is not None
