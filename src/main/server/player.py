"""Module for the player object"""


class Player:
    """class for the player object"""

    def __init__(self, name):
        super()
        self.name = name
        self.character = None

    def get_name(self):
        """returns name of player"""
        return self.name

    def get_character(self):
        """returns the character"""
        return self.character

    def set_character(self, character):
        """sets the character"""
        self.character = character
