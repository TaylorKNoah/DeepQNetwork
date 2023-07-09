from game import Game
from agent import Agent
import numpy as np
from GraphUtils import PlotScorePerGame, PlotMovesPerGame, PlotAverageScorePerMovePerGame

board_size = 4
num_cans = 16
num_games = 768
ep_dec = 0.9 / (0.8 * num_games)
bs = 8
filenames = ['Agents_Score_Per_Game_input6_output6.png', 'Agents_Moves_Per_Game_input6_output6.png', 'Agent_Average_Score_Per_Move_Per_Game_input6_output6.png']


if __name__ == '__main__':
	env = Game(board_size, num_cans)
	agent = Agent(gamma=0.99, epsilon=1.0, lr=0.003, input_dims=[5], batch_size=bs, n_actions=5,
								max_mem_size=10000, eps_end=0.1, eps_dec=ep_dec)
	scores, epsilon_history = [], []
	n_games = num_games
	total_moves = 0
	score_per_game, moves_per_game, avg_score_per_move_per_game = [], [], []

	for game in range(n_games):
		current_scores = []
		score = 0
		done = False
		observation = env.reset()
		move = 0

		while not done:
			action = agent.choose_action(observation)
			reward, new_observation, done = env.step(action)
			score += reward
			agent.store_transition(observation, action, reward, new_observation, done)

			#if move % 16 == 0: agent.learn()
			observation = new_observation
			scores.append(score)
			current_scores.append(score)
			epsilon_history.append(agent.epsilon)

			avg_score = np.mean(scores[-4*board_size:])

			#print('Move ', move, ') Score: %2f' %score, ', Average Score: %2f' %avg_score,
					#	', Epsilon Value: %2f' %agent.epsilon)
			
			move += 1
			if move > 200: done = True
			total_moves += 1
		agent.learn()
		
		walls = current_scores.count(-5)
		if game % 1 == 0 or game == num_games-1:
			print('Game ', game, ') -----------------> Total Score: ', int(score),' | Moves: ', move,'| ASM: ',int(score/move), ' | Walls: ',walls,' | EpsilonEnd: ',agent.epsilon)
		score_per_game.append(int(score))
		moves_per_game.append(move)
		avg_score_per_move_per_game.append(score/move)
		move = 0
		current_scores.clear()

x_axis = [i+1 for i in range(n_games)]
PlotScorePerGame(x_axis, score_per_game, filenames[0])
PlotMovesPerGame(x_axis, moves_per_game, filenames[1])
PlotAverageScorePerMovePerGame(x_axis, avg_score_per_move_per_game, filenames[2])
