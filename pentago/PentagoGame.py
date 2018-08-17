import sys
import numpy as np

sys.path.append('..')
from Game import Game
from .PentagoLogic import Board

from .PentagoUtilities import array_to_boardstr


class PentagoGame(Game):
    """
    Pentago Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, quadrant_size=None, win_length=None, np_pieces=None):
        Game.__init__(self)
        self._base_board = Board(quadrant_size, win_length, np_pieces)

    def getInitBoard(self):
        return self._base_board.np_pieces

    def getBoardSize(self):
        return (self._base_board.height, self._base_board.width)
    
    def getQuadrantSize(self):
        return (self._base_board.quadrant_size)

    def getActionSize(self):
        return self._base_board.height * self._base_board.width * 8

    def getNextState(self, board, player, action):
        """Returns a copy of the board with updated move, original board is unmodified."""
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        b.execute_move(action, player)
        return b.np_pieces, -player

    def getValidMoves(self, board, player):
        "Any zero value in top row in a valid move"
        b = self._base_board.with_np_pieces(np_pieces=board)
        moves = b.get_valid_moves()
        return [m in moves for m in b.move_names]
        

    def getGameEnded(self, board, player):
        b = self._base_board.with_np_pieces(np_pieces=board)
        winstate = b.get_win_state()
        if winstate.is_ended:
            if winstate.winner is None:
                # draw has very little value.
                return 1e-4
            elif winstate.winner == player:
                return +1
            elif winstate.winner == -player:
                return -1
            else:
                raise ValueError('Unexpected winstate found: ', winstate)
        else:
            # 0 used to represent unfinished game.
            return 0

    def getCanonicalForm(self, board, player):
        # Flip player from 1 to -1
        return board * player

    def getSymmetries(self, board, pi):
        """Board is left/right board symmetric"""
        # return [(board, pi), (board[:, ::-1], pi[::-1])]
        # mirror, rotational
        """
        n = 2*self._base_board.quadrant_size
        pi_board = np.reshape(pi[:-1], (n,n))
        sym = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                sym += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return sym
        """
        return [(board, pi)]

    def stringRepresentation(self, board):
        return str(self._base_board.with_np_pieces(np_pieces=board))


def display(board):
    print(array_to_boardstr(board))
