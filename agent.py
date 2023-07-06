import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

class DeepQNetwork(nn.Module):
	def __init__(self, learning_rate, input_dims, fullyConnected1_dims, fullyConnected2_dims, number_of_actions):
		super(DeepQNetwork, self).__init__()

		self.input_dims = input_dims
		self.fullyConnected1_dims = fullyConnected1_dims
		self.fullyConnected2_dims = fullyConnected2_dims
		self.n_actions = number_of_actions

		self.fc1 = nn.Linear(*self.input_dims, self.fullyConnected1_dims)
		self.fc2 = nn.Linear(self,fullyConnected1_dims, self.fullyConnected2_dims)
		self.fc3 = nn.Linear(self.fullyConnected2_dims, self.n_actions)

		self.optimizer = optim.Adam(self.paramters(), lr = learning_rate)
		self.loss = nn.MSELoss()
		self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
		self.to(self.device)

	def forward(self, state):
		x = F.relu(self.fc1(state))
		x = F.relu(self.fc2(x))
		actions = self.fc3(x)
		
		return actions

class Agent():
	def __init__(self, gamma, epsilon, lr, input_dims, batch_size, n_actions, max_mem_size=10000, eps_end=0.01, eps_dec=5e-4):
		# hyper params
		self.gamma = gamma
		self.epsilon = epsilon
		self.eps_min = eps_end
		self.eps_dec = eps_dec
		self.lr = lr

		# q network for action choice
		self.Q_eval = DeepQNetwork(learning_rate=lr, input_dims=input_dims, fullyConnected1_dims=16, fullyConnected2_dims=16, number_of_actions=5)

		# replay memory setup
		self.action_space = [i for i in range(n_actions)]
		self.mem_size = max_mem_size
		self.batch_size = batch_size
		self.mem_counter = 0

		# replay memory core (SARS memory)
		self.state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
		self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
		self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
		self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
		self.terminal_memory = np.seros(self.mem_size, dtype=np.bool)

	def store_transition(self, state, action, reward, new_state, done):
		first_unused_memory_index = self.mem_counter % self.mem_size
		# SARS
		self.state_memory[first_unused_memory_index] = state
		self.action_memory[first_unused_memory_index] = action
		self.reward_memory[first_unused_memory_index] = reward
		self.new_state_memory[first_unused_memory_index] = new_state
		self.terminal_memory[first_unused_memory_index] = done

		self.mem_counter += 1

	def choose_action(self, observation):
		if np.random.random() > self.epsilon:
			state = T.tensor([observation]).to(self.Q_eval.device)
			actions = self.Q_eval.forward(state)
			action = T.argmax(actions).item()
		else:
			action = np.random.choice(self.action_space)
		return action

	def learn(self):
		if self.mem_counter < self.batch_size:
			return

		self.Q_eval.optimizer.zero_grad()

		max_mem = min(self.mem_counter, self.mem_size)
		batch = np.random.choice(max_mem, self.batch_size, replace=False)

		batch_index = np.arange(self.batch_size, dtype=np.int32)

		state_batch = T.tensor(self.state_memory[batch]).to(self.Q_eval.device)
		new_state_batch = T.tensor(self.new_state_memory[batch]).to(self.Q_eval.device)
		reward_batch = T.tensor(self.reward_memory[batch]).to(self.Q_eval.device)
		terminal_batch = T.tensor(self.terminal_memory[batch]).to(self.Q_eval.device)
		action_batch = self.action_memory[batch]

		q_eval = self.Q_eval.forward(state_batch)[batch_index, action_batch]
		q_next = self.Q_eval.forward(new_state_batch)
		q_next[terminal_batch] = 0.0

		q_target = reward_batch + self.gamma * T.max(q_next, dim=1)[0]

		loss = self.Q_eval.loss(q_target, q_eval).to(self.Q_eval.device)
		loss.backward()
		self.Q_eval.optimizer.step()

		epsilon = self.epsilon - self.eps_dec if self.epsilon > self.eps_min else self.eps_min