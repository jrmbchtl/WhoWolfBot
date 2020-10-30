from enum import Enum


class TeamType(Enum):
	WERWOLF = 1,
	VILLAGER = 2,
	NONE = 0


# negative means prior to werwolf, positiv
class CharacterType(Enum):
	WERWOLF = 1,
	WOLFSHUND = -10,
	TERRORWOLF = 2,
	DORFBEWOHNER = 100,
	DORFBEWOHNERIN = 101,
	HEXE = 3,
	JAEGER = 102,
	SEHERIN = 4,
	NONE = 0
