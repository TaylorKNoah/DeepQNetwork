from game import Game
from agent import Agent
import numpy as np

if __name__ == '__main__':
	env = Game()
	agent = Agent(gamma=0.99, epsilon=1.0, lr=0.003, input_dims=5, batch_size=8, n_actions=5,
								max_mem_size=10000, eps_end=0.1, eps_dec=0.0005)
	scores, eps_history = [], []
	n_games = 16

	for i in range(n_games):
		score = 0
		done = False
		observation = env.reset()
		while not done:
			action = agent.choose_action(observation)
			new_observation, reward, done, info = env.step()
			score += reward
			agent.store_transition(observation, action, reward, new_observation, done)

			agent.learn()
			observation = new_observation
			scores.append(score)
			eps_history.append(agent.epsilon)

			avg_score = np.mean(scores[-4:])

			print('Episode ', i, ') Score: %2f' %score, ', Average Score: %2f' %avg_score,
						', Epsilon Value: %2f' %agent.epsilon)
		
		x = [i+1 for i in range(n_games)]
		filename = 'PickUpCans_AgentScorePlot'
		# plot_learning_curve(x, scores, eps_history, filename)