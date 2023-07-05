from enum import Enum

class Actions(Enum):
	PICK_UP = 0,
	MOVE_NORTH = 1,
	MOVE_EAST = 2,
	MOVE_SOUTH = 3,
	MOVE_WEST = 4

class BoardState(Enum):
	def __str__(self):
		return str(self.value)
	Empty = "E"
	Can = "C"
	Wall = "W"

