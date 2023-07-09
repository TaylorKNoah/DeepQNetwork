from random import randint
from enums import BoardState, Actions

class Game:
	map = []
	robotLocation = []
	numCans = 0

	def __init__(self, size=5, num_cans=15):
		self.size = size + 2
		#self.canDensity = canDensity
		self.numCans = num_cans
		self.numCansLeft = self.numCans
		self.initializeBoard()
		self.initializeStartPointOfRobot()
		return

	def initializeBoard(self):
		for i in range(0, self.size):
			row = []
			for j in range(0,self.size):
				if(self.isBorderWallTile(i, j)):
					row.append(BoardState.Wall)
				else:
					row.append(BoardState.Empty)
			self.map.append(row.copy())
			row.clear()
		self.addCansToMap()
		return

	def isBorderWallTile(self, i, j):
		if(i == 0 or j == 0 or i == self.size - 1 or j == self.size - 1):
			return True
		return False
	
	def addCansToMap(self):
		self.numCansLeft = self.numCans
		cans_to_add = self.numCansLeft
		while cans_to_add > 0:
			y = randint(1, self.size-2)
			x = randint(1, self.size-2)
			if(self.map[y][x] == BoardState.Can): continue
			self.map[y][x] = BoardState.Can
			cans_to_add -= 1


	
	'''
	def isCanTile(self):
		r = randint(0,100)/100
		if(r <= self.canDensity):
			return True
		return False
	'''


	def initializeStartPointOfRobot(self):
		for i in range(0,2):
			self.robotLocation.append(randint(1,self.size-2))

	def reset(self):
		self.map.clear()
		self.robotLocation.clear()
		self.initializeBoard()
		self.initializeStartPointOfRobot()
		return self.getState()
	
	def getState(self):
		rawState = []
		rawState.append(self.map[self.robotLocation[0]][self.robotLocation[1]].value)
		rawState.append(self.map[self.robotLocation[0]][self.robotLocation[1]-1].value)
		rawState.append(self.map[self.robotLocation[0]+1][self.robotLocation[1]].value)
		rawState.append(self.map[self.robotLocation[0]][self.robotLocation[1]+1].value)
		rawState.append(self.map[self.robotLocation[0]-1][self.robotLocation[1]].value)

		state = []
		for cell in rawState:
			if cell == BoardState.Can.value[0]:
				state.append(0)
			elif cell == BoardState.Empty.value[0]:
				state.append(1)
			else:
				state.append(2)
		return state.copy()

	def step(self, action):
		reward = self.determineReward(action)
		new_state = self.applyAction(action)
		done = self.isDone()
		return reward, new_state, done
		
	def determineReward(self, action):
		loc = self.robotLocation
		if action == 0:
			if self.map[loc[0]][loc[1]] == BoardState.Can:
				reward = 10
			else:
				reward = -5
		else:
			ymod = 0
			xmod = 0
			if action == 1: ymod -= 1
			elif action == 2: ymod += 1
			elif action == 3: xmod -= 1
			elif action == 4: xmod += 1
			if self.map[loc[0]+ymod][loc[1]+xmod] == BoardState.Wall:
				reward = -5
			else:
				reward = -1
		return reward
	
	def applyAction(self, action):
		y = self.robotLocation[0]
		x = self.robotLocation[1]

		if action == 0:
			if self.map[y][x] == BoardState.Can:
				self.map[y][x] = BoardState.Empty
				self.numCansLeft -= 1
		elif action == 1 and self.map[y-1][x] != BoardState.Wall:
				self.robotLocation[0] -= 1
		elif action == 2 and self.map[y+1][x] != BoardState.Wall:
			self.robotLocation[0] += 1
		elif action == 3 and self.map[y][x-1] != BoardState.Wall:
			self.robotLocation[1] -= 1
		elif action == 4 and self.map[y][x+1] != BoardState.Wall:
			self.robotLocation[1] += 1
		
		return self.getState()

	def isDone(self):
		return False if self.numCansLeft > 0 else True

	def displayBoard(self):
		print('\n')
		for i in range(0, self.size):
			for j in range(0, self.size):
				if(j < self.size - 1):
					if(i == self.robotLocation[0] and j == self.robotLocation[1]):
						print(self.map[i][j].value, end="R ")
					else:
						print(self.map[i][j].value, end="  ")
				else:
					print(self.map[i][j].value)



'''# test area
game = Game(4,16)
game.displayBoard()
print(game.numCans)'''