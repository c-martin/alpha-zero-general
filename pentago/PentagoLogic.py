from collections import namedtuple
from itertools import product
import numpy as np

DEFAULT_QUADRANT_SIZE = 3
DEFAULT_WIN_LENGTH = 5

Q = ['A','B','C','D']
D = ['+','-']
Qn = dict(zip(Q,[0,1,2,3]))
Dn = dict(zip(D,[-1,1]))
		
WinState = namedtuple('WinState', 'is_ended winner')

class Board():
	"""
	Pentago Board.
	"""

	def __init__(self, quadrant_size=None, win_length=None, np_pieces=None):
		"Set up initial board configuration."
		self.quadrant_size = quadrant_size or DEFAULT_QUADRANT_SIZE
		self.height = self.quadrant_size*2
		self.width = self.quadrant_size*2
		self.win_length = win_length or DEFAULT_WIN_LENGTH
		
		P = list(range(1,1+self.quadrant_size**2))
		self.move_names = [''.join(map(str,m)) for m in product(Q,P,Q,D)]

		move_coords = []
		dx = [0,0,self.quadrant_size,self.quadrant_size]
		dy = [0,self.quadrant_size,0,self.quadrant_size]
		for move in self.move_names:
			x,y = np.unravel_index(int(move[1])-1, (self.quadrant_size, self.quadrant_size))
			move_coords.append((x+dx[Qn[move[0]]], y+dy[Qn[move[0]]]))
		self.move_coords = move_coords

		if np_pieces is None:
			self.np_pieces = np.zeros([self.height, self.width])
		else:
			self.np_pieces = np_pieces
			assert self.np_pieces.shape == (self.height, self.width)
		
	def execute_move(self, move, player):
		"Move is a string: 'qXqD', where q=[A,B,C,D], X=keypad(1-9), D=+/-"
		if type(move) != str:
			move = self.move_names[move]
			
		x,y = np.unravel_index(int(move[1])-1, (self.quadrant_size, self.quadrant_size))
		move_q = Qn[move[0].upper()]
		turn_q = Qn[move[2].upper()]
		
		upper_half = np.hsplit(np.vsplit(self.np_pieces, 2)[0], 2)
		lower_half = np.hsplit(np.vsplit(self.np_pieces, 2)[1], 2)
		quads = np.concatenate([upper_half, lower_half])
		if quads[move_q][x][y] != 0:
			raise ValueError("Can't play (Row %d, Col %d) in quadrant %s" % (x,y,move[0].upper()))
		quads[move_q][x][y] = player
		quads[turn_q] = np.rot90(quads[turn_q], Dn[move[3]])
		upper_half = np.hstack([quads[0],quads[1]])
		lower_half = np.hstack([quads[2],quads[3]])
		self.np_pieces = np.vstack([upper_half, lower_half])

	def get_valid_moves(self):
		"Any zero value is a valid move"
		moves = [m for (m,xy) in zip(self.move_names, self.move_coords) if self.np_pieces[xy]==0]
		#flags = [self.np_pieces[xy] == 0 for xy in self.move_coords]
		#xylist = [xy for xy in self.move_coords if self.np_pieces[xy]==0]
		return moves

	def get_win_state(self):
		for player in [-1, 1]:
			player_pieces = self.np_pieces == -player
			# Check rows & columns for win
			if (self._is_straight_winner(player_pieces) or
				self._is_straight_winner(player_pieces.transpose()) or
				self._is_diagonal_winner(player_pieces)):
				return WinState(True, -player)

		# draw has very little value.
		if not any(self.get_valid_moves()):
			return WinState(True, None)

		# Game is not ended yet.
		return WinState(False, None)

	def with_np_pieces(self, np_pieces):
		"""Create copy of board with specified pieces."""
		if np_pieces is None:
			np_pieces = self.np_pieces
		return Board(self.quadrant_size, self.win_length, np_pieces)

	def _is_diagonal_winner(self, player_pieces):
		"""Checks if player_pieces contains a diagonal win."""
		win_length = self.win_length
		for i in range(len(player_pieces) - win_length + 1):
			for j in range(len(player_pieces[0]) - win_length + 1):
				if all(player_pieces[i + x][j + x] for x in range(win_length)):
					return True
			for j in range(win_length - 1, len(player_pieces[0])):
				if all(player_pieces[i + x][j - x] for x in range(win_length)):
					return True
		return False

	def _is_straight_winner(self, player_pieces):
		"""Checks if player_pieces contains a vertical or horizontal win."""
		run_lengths = [player_pieces[:, i:i + self.win_length].sum(axis=1)
					   for i in range(len(player_pieces) - self.win_length + 2)]
		return max([x.max() for x in run_lengths]) >= self.win_length

	def __str__(self):
		return str(self.np_pieces)
