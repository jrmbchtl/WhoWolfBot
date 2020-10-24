from enum import Enum


class TeamType(Enum):
	WERWOLF = 1,
	VILLAGER = 2,
	NONE = 0


class CharacterType(Enum):
	WERWOLF = 20,
	WOLFSHUND = 2,
	TERRORWOLF = 3,
	DORFBEWOHNER = 4,
	DORFBEWOHNERIN = 5,
	HEXE = 6,
	JAEGER = 7,
	SEHERIN = 8,
	NONE = 0
