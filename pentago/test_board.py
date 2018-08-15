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

def list_to_line(vals):
	assert(len(vals)==6)
	line = list(double_V + ((' '*3 + single_V )*2 + ' '*3 + double_V)*2)
	for i,v in enumerate(vals):
		line[2+4*i] = str(v)
	return ''.join(line)

def lines_to_board(lines):
	assert(len(lines)==6)
	board = '  ' + top + '  \n  '
	board += list_to_line(lines[0]) + '\n  ' + line_single + '\n  '
	board += list_to_line(lines[1]) + '\n  ' + line_single + '\n  '
	board += list_to_line(lines[2]) + '\n  ' + line_double + '\n  '
	board += list_to_line(lines[3]) + '\n  ' + line_single + '\n  '
	board += list_to_line(lines[4]) + '\n  ' + line_single + '\n  '
	board += list_to_line(lines[5]) + '\n  ' + bottom
	board = ' A' + ' '*25 + 'B\n' + board + '\n C' + ' '*25 + 'D\n'
	return(board)
	
def lines_to_quads(lines):
	q1 = [line[:3] for line in lines[:3]]
	q2 = [line[3:] for line in lines[:3]]
	q3 = [line[:3] for line in lines[3:]]
	q4 = [line[3:] for line in lines[3:]]
	return [q1, q2, q3, q4]

def quads_to_lines(quads):
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

def rotate_quadrant(lines, q, dir=1):
	quads = lines_to_quads(lines)
	if dir == 1:
		quads[q] = rotate_array_cw(quads[q])
	elif dir == -1:
		quads[q] = rotate_array_ccw(quads[q])
	return quads_to_lines(quads)
	

lines = [[1,2,3]*2, [4,5,6]*2, [7,8,9]*2]*2
board = lines_to_board(lines)
print('Example board:')
print(board)

print('Rotate top right CW and bottom left CCW:')
lines = rotate_quadrant(lines, 1, 1)
lines = rotate_quadrant(lines, 2, -1)
print(lines_to_board(lines))
