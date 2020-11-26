from enum import Enum


class TeamType(Enum):
	WEREWOLF = 1,
	VILLAGER = 2,
	WHITEWOLF = 3,
	NONE = 0


# negative means prior to werewolf, positive
class CharacterType(Enum):
	WOLFDOG = -10,
	CUPID = -8,
	NONE = 0
	WEREWOLF = 1,
	WHITEWOLF = 2,
	WITCH = 3,
	SEER = 4,
	BERSERK = 5,
	VILLAGER = 100,
	VILLAGERF = 101,
	HUNTER = 102,
	BADDASSBASTARD = 103,
	TERRORWOLF = 104,
	REDHAT = 104,
