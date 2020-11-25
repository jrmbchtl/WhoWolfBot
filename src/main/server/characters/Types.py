from enum import Enum


class TeamType(Enum):
	WEREWOLF = 1,
	VILLAGER = 2,
	NONE = 0


# negative means prior to werewolf, positive
class CharacterType(Enum):
	WEREWOLF = 1,
	WOLFDOG = -10,
	TERRORWOLF = 2,
	VILLAGER = 100,
	VILLAGERF = 101,
	WITCH = 3,
	HUNTER = 102,
	BADDASSBASTARD = 103,
	REDHAT = 104,
	SEER = 4,
	NONE = 0
