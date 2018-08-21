from Coach import Coach
from pentago.PentagoGame import PentagoGame as Game
from pentago.keras.NNet import NNetWrapper as nn
from utils import *

args = dotdict({
    'numIters': 100,
    'numEps': 100,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 90000,
    'arenaCompare': 50,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': True,
    #'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'load_folder_file': ('./temp/','checkpoint_37.pth.tar'),
    'numItersForTrainExamplesHistory': 50,

})

if __name__=="__main__":
    g = Game()
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
