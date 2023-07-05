from enum import Enum
from random import randint
import math
from typing import List
from enums import BoardState, Actions

class Agent:
	'''
	Input Shape / Contents
		0-4: contents of nearest (CNESW) tiles
		ideas for future nuerons
			1: known number of remaining cans?

	Output Shape / Contents
		5 total: one for each action
	Hidden Neurons
		L1: 8 Neurons

	Backpropagation:
		to get gradient to bp with: use "true best action"
			ie: randomly pick one of the best possible actions at random as the correct answer (unless the model picked one)
		could normalize the outputs and then say the optimal should be 1 and the rest 0.
			probably shoudl really do this
	'''

	def __init__(self):
		self.numInputNeurons = 5
		self.numHiddenL1 = 8
		self.numHiddenL2 = 8
		self.numOutputNeurons = 5

		self.neuronsInput: List[int] = []
		self.neuronsHiddenL1: List[int] = []
		self.neuronsHiddenL2: List[int] = []
		self.neuronsOutput: List[int] = []

		self.weightsL1In = []
		self.weightsL2L1 = []
		self.weightsOutL2 = []

		self.initNeurons()
		self.initWeights()
	
	def initNeurons(self):
		self.initInputNeurons()
		self.initHiddenNeurons()
		self.initOutputNeurons()
	
	def initInputNeurons(self):
		self.neuronsInput.append(1)
		for i in range(0, self.numInputNeurons):
			self.neuronsInput.append(0)
	
	def initHiddenNeurons(self):
		self.initHiddenL1Neurons()
		self.initHiddenL2Neurons()
	
	def initHiddenL1Neurons(self):
		for i in range(0, self.numHiddenL1):
			self.neuronsHiddenL1.append(0)

	def initHiddenL2Neurons(self):
		for i in range(0, self.numHiddenL2):
			self.neuronsHiddenL2.append(0)
			
	def initOutputNeurons(self):
		for i in range(0, self.numOutputNeurons):
			self.neuronsOutput.append(0)

	'''
			self.weightsL1In = []
			self.weightsL2L1 = []
			self.weightsOutL2 = []
	'''
	def initWeights(self):
		self.initWeightsL1In()
		self.initWeightsL2L1()
		self.initWeightsOutL2()

	def initWeightsL1In(self):
		for i in range(0, self.numHiddenL1):
			row = []
			for j in range(0, self.numInputNeurons):
				r = randint(-50, 50) / 100
				row.append(r)
			self.weightsL1In.append(row.copy())
			row.clear()

	def initWeightsL2L1(self):
		for i in range(0, self.numHiddenL2):
			row = []
			for j in range(0, self.numHiddenL1):
				r = randint(-50, 50) / 100
				row.append(r)
			self.weightsL2L1.append(row.copy())
			row.clear()
	
	def initWeightsOutL2(self):
		for i in range(0, self.numOutputNeurons):
			row = []
			for j in range(0, self.numHiddenL2):
				r = randint(-50, 50) / 100
				row.append(r)
			self.weightsOutL2.append(row.copy())
			row.clear()

	def displayWeights(self):
		print('Input --> Hidden L1 Weights')
		for i in range(len(agent.weightsL1In)):
			print(self.weightsL1In[i])
		
		print('Hidden1 --> Hidden2')
		for i in range(len(agent.weightsL2L1)):
			print(self.weightsL2L1[i])
		
		print('Hidden2 --> Output')
		for i in range(len(agent.weightsOutL2)):
			print(self.weightsOutL2[i])

	def observeState(self, state: List[BoardState]):
		interpretableState = self.scanEnvironment(state)
		for i in range(self.numInputNeurons):
			self.neuronsInput[i] = interpretableState[i]
	
	def scanEnvironment(self, state: List[BoardState]) -> List[int]:
		interpretableState: List[int] = []
		for i in range(len(state)):
			interpretableState.append(self.interperateBoardStateValue(state[i]))
		return interpretableState
	
	def interperateBoardStateValue(self, boardState: BoardState) -> int:
		if boardState == BoardState.Empty: return 0
		if boardState == BoardState.Can: return 1
		if boardState == BoardState.Wall: return 2
	
	def chooseAction(self) -> Actions:
		self.forwardPropagate()
		return self.bestAction()

	def bestAction(self) -> Actions:
		bestScore = -1000000
		bestAction = Actions.PICK_UP
		for i in range(self.numOutputNeurons):
			if self.neuronsOutput[i] > bestScore:
				bestAction = self.getAction(i)
				bestScore = self.neuronsOutput[i]
		return bestAction
	
	def getAction(self, i):
		if(i == 0): return Actions.PICK_UP
		if(i == 1): return Actions.MOVE_NORTH
		if(i == 2): return Actions.MOVE_EAST
		if(i == 3): return Actions.MOVE_SOUTH
		if(i == 4): return Actions.MOVE_WEST

	def forwardPropagate(self):
		self.forwardPropagateToHiddenL1()
		self.forwardPropagateToHiddenL2()
		self.forwardPropagateToOutput()
	
	def forwardPropagateToHiddenL1(self):
		for i in range(self.numHiddenL1):
			hiddenSum = 0
			for j in range(self.numInputNeurons):
				hiddenSum += self.neuronsInput[j] * self.weightsL1In[i][j]
			self.neuronsHiddenL1[i] = self.sigmoidActivation(hiddenSum)

	def forwardPropagateToHiddenL2(self):
		for i in range(self.numHiddenL2):
			hiddenSum = 0
			for j in range(self.numHiddenL1):
				hiddenSum += self.neuronsHiddenL1[j] * self.weightsL2L1[i][j]
			self.neuronsHiddenL2[i] = self.sigmoidActivation(hiddenSum)

	def forwardPropagateToOutput(self):
		for i in range(self.numOutputNeurons):
			outputSum = 0
			for j in range(self.numHiddenL2):
				outputSum += self.neuronsHiddenL2[j] * self.weightsOutL2[i][j]
			self.neuronsOutput[i] = outputSum
		self.normalizeOutputs()
	
	def normalizeOutputs(self):
		# ensure all outputs are positive by add smallest to all
		least = min(self.neuronsOutput)
		if least < 0: 
			for k in range(0, len(self.neuronsOutput)): self.neuronsOutput[k] += least*-1

		outputsSum = sum(self.neuronsOutput)
		normOutputs = [float(i)/outputsSum for i in self.neuronsOutput]
		self.neuronsOutput = normOutputs.copy()
	
	def sigmoidActivation(self, x: float) -> float:
		negx = x * -1
		enegx = math.exp(negx)
		openegx = 1 + enegx
		final = 1 / openegx
		return final
	
	# test area
agent = Agent()
agent.displayWeights()
state = [BoardState.Can, BoardState.Wall, BoardState.Wall, BoardState.Empty, BoardState.Empty] 
agent.observeState(state)
action = agent.chooseAction()
print(agent.neuronsOutput)
print(action)
