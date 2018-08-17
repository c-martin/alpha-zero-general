import numpy as np


class RandomPlayer():
	def __init__(self, game):
		self.game = game

	def play(self, board):			
		valids = self.game.getValidMoves(board, 1)
		id = int(np.random.choice(np.where(valids)[0]))
		return id


class HumanPentagoPlayer():
	def __init__(self, game):
		self.game = game

	def play(self, board):
		valids = self.game.getValidMoves(board, 1)
		moves = self.game._base_board.with_np_pieces(np_pieces=board).move_names
		
		print('\nEnter a move: ')
		while True:
			move = input().upper()
			if move in moves:
				id = moves.index(move)
				if valids[id]: break
				else: print('Illegal move, please choose a different move: ')
			else:
				id = int(np.random.choice(np.where(valids)[0]))
				print('Invalid move, please enter a move like ' + moves[id] + ':')
		return id


class OneStepLookaheadPentagoPlayer():
	"""Simple player who always takes a win if presented, or blocks a loss if obvious, otherwise is random."""
	def __init__(self, game, verbose=True):
		self.game = game
		self.player_num = 1
		self.verbose = verbose

	def play(self, board):
		valid_moves = self.game.getValidMoves(board, self.player_num)
		win_move_set = set()
		fallback_move_set = set()
		stop_loss_move_set = set()
		for move, valid in enumerate(valid_moves):
			if not valid: continue
			if self.player_num == self.game.getGameEnded(*self.game.getNextState(board, self.player_num, move)):
				win_move_set.add(move)
			if -self.player_num == self.game.getGameEnded(*self.game.getNextState(board, -self.player_num, move)):
				stop_loss_move_set.add(move)
			else:
				fallback_move_set.add(move)

		if len(win_move_set) > 0:
			ret_move = np.random.choice(list(win_move_set))
			if self.verbose: print('Playing winning action %s from %s' % (ret_move, win_move_set))
		elif len(stop_loss_move_set) > 0:
			ret_move = np.random.choice(list(stop_loss_move_set))
			if self.verbose: print('Playing loss stopping action %s from %s' % (ret_move, stop_loss_move_set))
		elif len(fallback_move_set) > 0:
			ret_move = np.random.choice(list(fallback_move_set))
			if self.verbose: print('Playing random action %s from %s' % (ret_move, fallback_move_set))
		else:
			raise Exception('No valid moves remaining: %s' % game.stringRepresentation(board))

		return ret_move
