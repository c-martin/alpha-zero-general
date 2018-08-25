import Arena
from MCTS import MCTS
from pentago.PentagoGame import PentagoGame, display
from pentago.PentagoPlayers import *
from pentago.keras.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = PentagoGame()

# all players
rp = RandomPlayer(g).play
hp = HumanPentagoPlayer(g).play

# nnet players
def nn_player_from_ckpt(g, path='./pretrained_models/pentago/keras/', filename='best.pth.tar'):
	nn = NNet(g)
	nn.load_checkpoint(path, filename)
	args = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
	mcts = MCTS(g, nn, args)
	nnp = lambda x: np.argmax(mcts.getActionProb(x, temp=0))
	return nnp

n1p = nn_player_from_ckpt(g, filename='checkpoint_81.pth.tar')
n2p = nn_player_from_ckpt(g, filename='checkpoint_40.pth.tar')

play_network = Arena.Arena(n1p, hp, g, display=display)
test_network = Arena.Arena(n1p, rp, g, display=display)
pit_networks = Arena.Arena(n1p, n2p, g, display=display)
play_random = Arena.Arena(hp, rp, g, display=display)
test_random = Arena.Arena(rp, rp, g, display=display)
print(play_network.playGames(2, verbose=True))
#print(pit_networks.playGames(100, verbose=False))
#print(test_network.playGames(20, verbose=False))
