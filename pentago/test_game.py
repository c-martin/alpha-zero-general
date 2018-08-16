import numpy as np
from PentagoLogic import Board
from PentagoUtilities import array_to_boardstr

mask1 = np.random.binomial(1,0.2,[6,6]) == 1
mask2 = np.random.binomial(1,0.2,[6,6]) == 1
pieces = np.zeros([6,6], dtype=int) + mask1 - mask2

board = Board(np_pieces = pieces)
print('Initial board:\n' + array_to_boardstr(board.np_pieces) + '\n')
player = 1
turns = 0

win = board.get_win_state()
while not win[0]:
    turns += 1
    moves = [m for (m,xy) in zip(board.move_names, board.move_coords) if board.np_pieces[xy]==0]
    move = np.random.choice(moves)
    board.execute_move(move, player)
    print('Executing move ' + move + ' for player ' + {1:'X',-1:'O'}[player] + ':\n' + array_to_boardstr(board.np_pieces) + '\n')
    win = board.get_win_state()
    player = -player

print('Game ended in ' + str(turns) + ' moves, won by player ' + {1:'X',-1:'O'}[win[1]] + '\n')
