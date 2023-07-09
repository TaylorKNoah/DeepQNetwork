import numpy as np
from matplotlib import pyplot as plt


def PlotScorePerGame(x_axis, scores, filename):
	fig, ax = plt.subplots()
	ax.plot(x_axis, scores)

	ax.set(xlabel='Games', ylabel='Score', title='Agent\'s Score Per Game')
	ax.grid()

	fig.savefig(filename)
	plt.show()

def PlotMovesPerGame(x_axis, moves, filename):
	fig, ax = plt.subplots()
	ax.plot(x_axis, moves)

	ax.set(xlabel='Games', ylabel='Moves', title='Agent\'s Moves Per Game')
	ax.grid()

	fig.savefig(filename)
	plt.show()

def PlotAverageScorePerMovePerGame(x_axis, avg_scores_per_move_per_game, filename):
	fig, ax = plt.subplots()
	ax.plot(x_axis, avg_scores_per_move_per_game)

	ax.set(xlabel='Games', ylabel='Moves', title='Agent\'s Average Score Per Move Per Game')
	ax.grid()

	fig.savefig(filename)
	plt.show()