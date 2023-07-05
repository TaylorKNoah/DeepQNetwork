from random import randint
from enums import BoardState, Actions

class Game:
	map = []
	robotLocation = []
	numCans = 0

	def __init__(self, size=8, canDensity=0.25, maxWallLength=4, wallDensity=0.8):
		self.size = size
		self.canDensity = canDensity
		self.maxWallLength = maxWallLength
		self.wallDensity = wallDensity
		self.initializeBoard()
		self.initializeStartPointOfRobot()
		return

	def initializeBoard(self):
		for i in range(0, self.size):
			row = []

			for j in range(0,self.size):
				if(self.isBorderWallTile(i, j)):
					row.append(BoardState.Wall)
				elif(self.isCanTile()):
					row.append(BoardState.Can)
					self.numCans += 1
				else:
					row.append(BoardState.Empty)
			self.map.append(row.copy())

			row.clear()
		return

	def isBorderWallTile(self, i, j):
		if(i == 0 or j == 0 or i == self.size - 1 or j == self.size - 1):
			return True
		return False

	def isCanTile(self):
		r = randint(0,100)/100
		if(r <= self.canDensity):
			return True
		return False

	def initializeStartPointOfRobot(self):
		for i in range(0,2):
			self.robotLocation.append(randint(1,self.size-2))
		print("Robot start at: ", end=" ")
		print(self.robotLocation)

	def playGame(self):
		self.displayStart()
		while(self.numCans > 0):
			self.displayRound()
			self.displayBoard()
			state = self.agent.observe(self.map)
			action = self.agent.decideAction(state)
			reward = self.determineReward(state, action)
			self.displayAgentInfo()

	def displayStart(self):
		print('========== Game Start! ==========')
		print('Number of cans to find: '+str(self.numCans))

	def displayRound(self, round):
		print('---------- Round '+str(round)+' ----------')

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
	
	def determineReward(self, state, action):
		reward = 0
		if(action == Actions.PICK_UP):
			if(state[0] == BoardState.Can):
				reward = 10
				self.map[self.robotLocation[0],self.robotLocation[1]] = BoardState.Empty
			else:
				reward = -5
