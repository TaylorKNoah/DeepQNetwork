from game import Game
from agent import Agent
import numpy as np

board_size = 4
can_density = 0.75
num_games = 48

if __name__ == '__main__':
	env = Game(board_size, can_density)
	agent = Agent(gamma=0.99, epsilon=1.0, lr=0.003, input_dims=[5], batch_size=8, n_actions=5,
								max_mem_size=10000, eps_end=0.1, eps_dec=0.0005)
	scores, eps_history = [], []
	n_games = num_games

	for i in range(n_games):
		print('===========================================================================')
		print('================================= Game ',i,'=================================')
		print('===========================================================================')
		score = 0
		done = False
		observation = env.reset()
		move = 0
		while not done:
			action = agent.choose_action(observation)
			reward, new_observation, done = env.step(action)
			score += reward
			agent.store_transition(observation, action, reward, new_observation, done)

			agent.learn()
			observation = new_observation
			scores.append(score)
			eps_history.append(agent.epsilon)

			avg_score = np.mean(scores[-4*board_size:])

			print('Move ', move, ') Score: %2f' %score, ', Average Score: %2f' %avg_score,
						', Epsilon Value: %2f' %agent.epsilon)
			
			move += 1
		
		x = [i+1 for i in range(n_games)]
		filename = 'PickUpCans_AgentScorePlot'
		# plot_learning_curve(x, scores, eps_history, filename)
		move = 0