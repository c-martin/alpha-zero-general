import numpy as np
import PentagoUtilities as util

mask1 = np.random.binomial(1,0.4,[6,6]) == 1
mask2 = np.random.binomial(1,0.4,[6,6]) == 1
pieces = np.zeros([6,6], dtype=int) + mask1 - mask2

print('Example board:')
print(util.array_to_boardstr(pieces))

print('Rotate top right CW and bottom left CCW:')
board = util.rotate_quadrant(pieces, 1, 1)
board = util.rotate_quadrant(pieces, 2, -1)
print(util.array_to_boardstr(pieces))
