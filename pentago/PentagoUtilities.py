# corners
double_DR = '\u2554'
double_DL = '\u2557'
double_UR = '\u255A'
double_UL = '\u255D'
# walls
double_H = '\u2550'
double_V = '\u2551'
single_H = '\u2500'
single_V = '\u2502'
# 4-way crosses
single_V_single_H = '\u253C'
single_V_double_H = '\u256A'
double_V_single_H = '\u256B'
double_V_double_H = '\u256C'
# 3-way crosses
double_V_single_R = '\u255F'
double_V_double_R = '\u2560'
double_V_single_L = '\u2562'
double_V_double_L = '\u2563'
double_H_single_U = '\u2567'
double_H_double_U = '\u2569'
double_H_single_D = '\u2564'
double_H_double_D = '\u2566'

symbols = {1 : 'X', -1 : 'O', 0 : ' '}
#symbols = {1 : '\u25CB', -1 : '\u25CF', 0 : ' '}

top = (double_DR + 
    double_H*3 + double_H_single_D +
    double_H*3 + double_H_single_D +
    double_H*3 + double_H_double_D +
    double_H*3 + double_H_single_D +
    double_H*3 + double_H_single_D +
    double_H*3 + double_DL)

line_single = (double_V_single_R + 
    single_H*3 + single_V_single_H + 
    single_H*3 + single_V_single_H + 
    single_H*3 + double_V_single_H + 
    single_H*3 + single_V_single_H + 
    single_H*3 + single_V_single_H + 
    single_H*3 + double_V_single_L)

line_double = (double_V_double_R + 
    double_H*3 + single_V_double_H + 
    double_H*3 + single_V_double_H + 
    double_H*3 + double_V_double_H + 
    double_H*3 + single_V_double_H + 
    double_H*3 + single_V_double_H + 
    double_H*3 + double_V_double_L)

bottom = (double_UR + 
    double_H*3 + double_H_single_U +
    double_H*3 + double_H_single_U +
    double_H*3 + double_H_double_U +
    double_H*3 + double_H_single_U +
    double_H*3 + double_H_single_U +
    double_H*3 + double_UL)

def list_to_rowstr(vals):
    # input list of values (0,1,-1), output string for row
    line = list(double_V + ((' '*3 + single_V )*2 + ' '*3 + double_V)*2)
    for i,v in enumerate(vals):
        line[2+4*i] = symbols[v]
    return ''.join(line)

def array_to_boardstr(arr):
    # input array of values (0,1,-1), output printable board
    board = '  ' + top + '  \n  '
    spacers = [line_single + '\n  ']*2 + [line_double + '\n  ']
    spacers += [line_single + '\n  ']*2 + [bottom]
    for i in range(6):
        board += list_to_rowstr(arr[i])
        board += '\n  ' + spacers[i]
    board = (' A' + ' '*25 + 'B\n' + board + '\n C' + ' '*25 + 'D\n')
    return(board)
    
def array_to_quads(arr):
    lines = [list(a) for a in arr]
    q1 = [line[:3] for line in lines[:3]]
    q2 = [line[3:] for line in lines[:3]]
    q3 = [line[:3] for line in lines[3:]]
    q4 = [line[3:] for line in lines[3:]]
    return [q1, q2, q3, q4]

def quads_to_array(quads):
    r1 = quads[0][0] + quads[1][0]
    r2 = quads[0][1] + quads[1][1]
    r3 = quads[0][2] + quads[1][2]
    r4 = quads[2][0] + quads[3][0]
    r5 = quads[2][1] + quads[3][1]
    r6 = quads[2][2] + quads[3][2]
    return [r1, r2, r3, r4, r5, r6]

def rotate_array_cw(arr):
    return [list(a) for a in zip(*arr[::-1])]

def rotate_array_ccw(arr):
    return [list(a) for a in zip(*arr)][::-1]

def rotate_quadrant(arr, q, dir):
    quads = array_to_quads(arr)
    if dir == 1:
        quads[q] = rotate_array_cw(quads[q])
    elif dir == -1:
        quads[q] = rotate_array_ccw(quads[q])
    return quads_to_array(quads)
    

import numpy as np

move_names = ['A1A+', 'A1A-', 'A1B+', 'A1B-', 'A1C+', 'A1C-', 'A1D+', 'A1D-', 'A2A+', 'A2A-', 'A2B+', 'A2B-', 'A2C+', 'A2C-', 'A2D+', 'A2D-', 'A3A+', 'A3A-', 'A3B+', 'A3B-', 'A3C+', 'A3C-', 'A3D+', 'A3D-', 'A4A+', 'A4A-', 'A4B+', 'A4B-', 'A4C+', 'A4C-', 'A4D+', 'A4D-', 'A5A+', 'A5A-', 'A5B+', 'A5B-', 'A5C+', 'A5C-', 'A5D+', 'A5D-', 'A6A+', 'A6A-', 'A6B+', 'A6B-', 'A6C+', 'A6C-', 'A6D+', 'A6D-', 'A7A+', 'A7A-', 'A7B+', 'A7B-', 'A7C+', 'A7C-', 'A7D+', 'A7D-', 'A8A+', 'A8A-', 'A8B+', 'A8B-', 'A8C+', 'A8C-', 'A8D+', 'A8D-', 'A9A+', 'A9A-', 'A9B+', 'A9B-', 'A9C+', 'A9C-', 'A9D+', 'A9D-', 'B1A+', 'B1A-', 'B1B+', 'B1B-', 'B1C+', 'B1C-', 'B1D+', 'B1D-', 'B2A+', 'B2A-', 'B2B+', 'B2B-', 'B2C+', 'B2C-', 'B2D+', 'B2D-', 'B3A+', 'B3A-', 'B3B+', 'B3B-', 'B3C+', 'B3C-', 'B3D+', 'B3D-', 'B4A+', 'B4A-', 'B4B+', 'B4B-', 'B4C+', 'B4C-', 'B4D+', 'B4D-', 'B5A+', 'B5A-', 'B5B+', 'B5B-', 'B5C+', 'B5C-', 'B5D+', 'B5D-', 'B6A+', 'B6A-', 'B6B+', 'B6B-', 'B6C+', 'B6C-', 'B6D+', 'B6D-', 'B7A+', 'B7A-', 'B7B+', 'B7B-', 'B7C+', 'B7C-', 'B7D+', 'B7D-', 'B8A+', 'B8A-', 'B8B+', 'B8B-', 'B8C+', 'B8C-', 'B8D+', 'B8D-', 'B9A+', 'B9A-', 'B9B+', 'B9B-', 'B9C+', 'B9C-', 'B9D+', 'B9D-', 'C1A+', 'C1A-', 'C1B+', 'C1B-', 'C1C+', 'C1C-', 'C1D+', 'C1D-', 'C2A+', 'C2A-', 'C2B+', 'C2B-', 'C2C+', 'C2C-', 'C2D+', 'C2D-', 'C3A+', 'C3A-', 'C3B+', 'C3B-', 'C3C+', 'C3C-', 'C3D+', 'C3D-', 'C4A+', 'C4A-', 'C4B+', 'C4B-', 'C4C+', 'C4C-', 'C4D+', 'C4D-', 'C5A+', 'C5A-', 'C5B+', 'C5B-', 'C5C+', 'C5C-', 'C5D+', 'C5D-', 'C6A+', 'C6A-', 'C6B+', 'C6B-', 'C6C+', 'C6C-', 'C6D+', 'C6D-', 'C7A+', 'C7A-', 'C7B+', 'C7B-', 'C7C+', 'C7C-', 'C7D+', 'C7D-', 'C8A+', 'C8A-', 'C8B+', 'C8B-', 'C8C+', 'C8C-', 'C8D+', 'C8D-', 'C9A+', 'C9A-', 'C9B+', 'C9B-', 'C9C+', 'C9C-', 'C9D+', 'C9D-', 'D1A+', 'D1A-', 'D1B+', 'D1B-', 'D1C+', 'D1C-', 'D1D+', 'D1D-', 'D2A+', 'D2A-', 'D2B+', 'D2B-', 'D2C+', 'D2C-', 'D2D+', 'D2D-', 'D3A+', 'D3A-', 'D3B+', 'D3B-', 'D3C+', 'D3C-', 'D3D+', 'D3D-', 'D4A+', 'D4A-', 'D4B+', 'D4B-', 'D4C+', 'D4C-', 'D4D+', 'D4D-', 'D5A+', 'D5A-', 'D5B+', 'D5B-', 'D5C+', 'D5C-', 'D5D+', 'D5D-', 'D6A+', 'D6A-', 'D6B+', 'D6B-', 'D6C+', 'D6C-', 'D6D+', 'D6D-', 'D7A+', 'D7A-', 'D7B+', 'D7B-', 'D7C+', 'D7C-', 'D7D+', 'D7D-', 'D8A+', 'D8A-', 'D8B+', 'D8B-', 'D8C+', 'D8C-', 'D8D+', 'D8D-', 'D9A+', 'D9A-', 'D9B+', 'D9B-', 'D9C+', 'D9C-', 'D9D+', 'D9D-']
move_coords = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 2), (0, 2), (0, 2), (0, 2), (0, 2), (0, 2), (0, 2), (0, 2), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 2), (1, 2), (1, 2), (1, 2), (1, 2), (1, 2), (1, 2), (1, 2), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 0), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 2), (2, 2), (2, 2), (2, 2), (2, 2), (2, 2), (2, 2), (2, 2), (0, 3), (0, 3), (0, 3), (0, 3), (0, 3), (0, 3), (0, 3), (0, 3), (0, 4), (0, 4), (0, 4), (0, 4), (0, 4), (0, 4), (0, 4), (0, 4), (0, 5), (0, 5), (0, 5), (0, 5), (0, 5), (0, 5), (0, 5), (0, 5), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 3), (1, 4), (1, 4), (1, 4), (1, 4), (1, 4), (1, 4), (1, 4), (1, 4), (1, 5), (1, 5), (1, 5), (1, 5), (1, 5), (1, 5), (1, 5), (1, 5), (2, 3), (2, 3), (2, 3), (2, 3), (2, 3), (2, 3), (2, 3), (2, 3), (2, 4), (2, 4), (2, 4), (2, 4), (2, 4), (2, 4), (2, 4), (2, 4), (2, 5), (2, 5), (2, 5), (2, 5), (2, 5), (2, 5), (2, 5), (2, 5), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 1), (3, 2), (3, 2), (3, 2), (3, 2), (3, 2), (3, 2), (3, 2), (3, 2), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 0), (4, 1), (4, 1), (4, 1), (4, 1), (4, 1), (4, 1), (4, 1), (4, 1), (4, 2), (4, 2), (4, 2), (4, 2), (4, 2), (4, 2), (4, 2), (4, 2), (5, 0), (5, 0), (5, 0), (5, 0), (5, 0), (5, 0), (5, 0), (5, 0), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 2), (5, 2), (5, 2), (5, 2), (5, 2), (5, 2), (5, 2), (5, 2), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 3), (3, 4), (3, 4), (3, 4), (3, 4), (3, 4), (3, 4), (3, 4), (3, 4), (3, 5), (3, 5), (3, 5), (3, 5), (3, 5), (3, 5), (3, 5), (3, 5), (4, 3), (4, 3), (4, 3), (4, 3), (4, 3), (4, 3), (4, 3), (4, 3), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 4), (4, 5), (4, 5), (4, 5), (4, 5), (4, 5), (4, 5), (4, 5), (4, 5), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 3), (5, 4), (5, 4), (5, 4), (5, 4), (5, 4), (5, 4), (5, 4), (5, 4), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5), (5, 5)]
move_quadrants = [name[2] for name in move_names]
move_directions = [{'+':-1, '-':1}[name[3]] for name in move_names]

# build list of rotated 1...36 arrays
arr = np.reshape(np.arange(36), (6,6))
rot_arr = []
for i in range(1,5): rot_arr.append( np.rot90(arr, -i) )
for i in range(1,5): rot_arr.append( np.fliplr(np.rot90(arr, -i)) )
# for reach symmetry, create list of permuted indexes
rot_xy = []
for i in range(8):
    rot_xy.append([np.unravel_index(i, (6,6)) for i in np.ravel(rot_arr[i])])

# rot_dict[QN][s] is QN after applying symmetry #s (r1,r2,r3,r4,r1s,r2s,r3s,r4s)
images = ['A','B','D','C', 'B','A','C','D']
rot_dict = {}
for q in ['A','B','D','C']:
    images = images[:4][1:] + images[:4][:1] + images[4:][1:] + images[4:][:1]
    rot_dict[q + '+'] = [''.join(s) for s in zip(images, ['+']*4 + ['-']*4)]
    rot_dict[q + '-'] = [''.join(s) for s in zip(images, ['-']*4 + ['+']*4)]

# lookup QN based on (x,y) as qkey[x][y],nkey[x][y]
qkey = [['A']*3 + ['B']*3]*3 + [['C']*3 + ['D']*3]*3
nkey = [[1,2,3]*2] + [[4,5,6]*2] + [[7,8,9]*2] + [[1,2,3]*2] + [[4,5,6]*2] + [[7,8,9]*2]

def rotate_move_name(move, n):
    # returns equivalent move on board with symmetry n
    dx,dy = [0,0,3,3],[0,3,0,3]
    x,y = np.unravel_index(int(move[1])-1, (3,3))
    x += dx[ dict(zip(['A','B','C','D'],[0,1,2,3]))[move[0]] ]
    y += dy[ dict(zip(['A','B','C','D'],[0,1,2,3]))[move[0]] ]
    (x_new, y_new) = np.unravel_index(rot_xy[n].index((x,y)), (6,6))
    q_new = qkey[x_new][y_new]
    n_new = nkey[x_new][y_new]
    r_new = rot_dict[ move[2:] ][n]
    return '%s%s%s' % (q_new, n_new, r_new)

def sym_board(board, n):
    board = np.rot90(board, (n%4)+1)
    if n>3: board = np.fliplr(board)
    return board

def sym_moves(vec, n):
    rotated_moves = [rotate_move_name(move,n) for move in move_names]
    return [vec[move_names.index(m)] for m in rotated_moves]