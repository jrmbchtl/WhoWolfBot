"""module for the different team types and character types"""
from enum import Enum


class TeamType(Enum):
    """enum for the different teams"""
    WEREWOLF = 1
    VILLAGER = 2
    WHITEWOLF = 3
    NONE = 0


# negative means prior to werewolf, positive
class CharacterType(Enum):
    """enum for the different characters"""
    WOLFDOG = -10
    CUPID = -8
    NONE = 0
    WEREWOLF = 1
    WHITEWOLF = 2
    WITCH = 3
    SEER = 4
    BERSERK = 5
    SCALLYWAG = 10
    PSYCHOPATH = 99
    VILLAGER = 100
    VILLAGERF = 101
    HUNTER = 102
    BADDASSBASTARD = 103
    TERRORWOLF = 104
    REDHAT = 105
