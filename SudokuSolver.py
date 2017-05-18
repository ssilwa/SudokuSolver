# Python Program to solve Sudoku by Constant Propogation and DFS
# Ideas based on this article: http://norvig.com/sudoku.html


import math
import copy
import time
import sys


Column = {}
Row = {}
Square = {}
All = {}
Family_Types = [Column, Row, Square]


for i in range(9):
	for j in range(9):
		Column[(i,j)] = [(k,j) for k in range(9)]
		Row[(i,j)] = [(i,k) for k in range(9)]
		Square[(i,j)] = []
		rowbox_min = 3*math.floor(i/3)
		colbox_min = 3*math.floor(j/3)
		for r in range(rowbox_min, rowbox_min + 3):
			for c in range(colbox_min, colbox_min + 3):
				Square[(i,j)].append((r,c))


Digits = [1,2,3,4,5,6,7,8,9]


def possibleval_maker(grid):
	PossibleVals = {}
	for i in range(9):
		for j in range(9):
			if grid[i][j] == '':
				Possibilities = copy.deepcopy(Digits)

				for name in Family_Types:
					for key in name[(i,j)]:
						if grid[key[0]][key[1]] != '':
							try:
								Possibilities.remove(grid[key[0]][key[1]])
							except:
								pass
				PossibleVals[(i,j)] = Possibilities
				if len(Possibilities) == 0:
					print('NOT POSSIBLE!')
			else:

				PossibleVals[(i,j)] = 'finished'

	return PossibleVals



def remover(index, val, PossibleVals):
	for name in Family_Types:
		for key in name[index]:

			try:
				PossibleVals[key].remove(val)
			except:
				pass
	return PossibleVals



def constantprop(grid, PossibleVals):
	keep_going = True
	while keep_going:
		keep_going = False

		for i in range(9):
			for j in range(9):

				if PossibleVals[(i,j)] != 'finished':

					if len(PossibleVals[(i,j)]) == 1:
						keep_going = True       					# keep going if you find a square whose value is fixed
						val = PossibleVals[(i,j)][0]
						grid[i][j] = val
						PossibleVals[(i,j)] = 'finished'
						PossibleVals = remover((i,j), val, PossibleVals)



					for d in Digits: 
						for name in Family_Types:
							count = 0
							current = None

							for key in name[(i,j)]:
								if PossibleVals[key] != 'finished':
									if d in PossibleVals[key]:
										count += 1
										current = key

							if count == 1:
								keep_going = True	
								grid[current[0]][current[1]] = d
								PossibleVals[current] = 'finished'
								PossibleVals = remover(current, d, PossibleVals)

	return (grid, PossibleVals)


def sudoku_checker(A): # Check if a filled sudoku is valid
	correct = True
	for i in range(9):
		for j in range(9):
			for name in Family_Types:
				for key in name[(i,j)]:
					if (i,j) != (key[0], key[1]):
						if A[i][j] == A[key[0]][key[1]]:
							correct = False

	return correct

def finished(Grid):
	finished = True
	for i in range(9):
		for j in range(9):
			if Grid[i][j] == '':
				finished = False
	return finished

def MinRemaining(PossibleVals):
	current = []
	index = None
	for key in PossibleVals:
		if len(PossibleVals[key]) > len(current) and PossibleVals[key] != 'finished':
			current = PossibleVals[key]
			index = key
	return index

def SudokuDFS(grid, PossibleVals):
	grid, PossibleVals = constantprop(grid, PossibleVals)

	if not finished(grid):
		index = MinRemaining(PossibleVals)
		children = []
		if index == None:
			return (0, None)
		else:
			for val in PossibleVals[index]:
				newgrid = copy.deepcopy(grid)
				newgrid[index[0]][index[1]] = val
				newpossval = copy.deepcopy(PossibleVals)
				newpossval[index] = 'finished'
				newpossval = remover(index, val, newpossval)
				children.append(SudokuDFS(newgrid, newpossval))
			best = max(children, key=lambda item:item[0])
			if best[0] == 1:   # Quit once you find a solution!
				Prettify(best[1])
				print("--- %s seconds ---" % (time.time() - start_time))
				sys.exit()
			return best

	elif not sudoku_checker(grid):
		return (0, None)

	else:
		return (1, grid)



def Prettify(Grid):
	prettygrid = copy.deepcopy(Grid)
	for i in range(9):
		for j in range(9):
			if prettygrid[i][j] == '':
				prettygrid[i][j] = "."
	print('-------------------------------------')
	for i in reversed(range(9)):
		print("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" %(prettygrid[i][0], prettygrid[i][1], prettygrid[i][2], prettygrid[i][3], prettygrid[i][4], prettygrid[i][5], prettygrid[i][6], prettygrid[i][7], prettygrid[i][8]))
		print('-------------------------------------')




# A = [['','', '', '','','','','',''], ['','','','','','','','',''], ['','','',3,2,5,'','',6], ['','',6,'','',3,'',5,4], ['','',3,'','','','','',''], ['',4,5,'','','','','',''],[2,'','','','',8,'','',''],['',5,9,'','','','','',8],['','','','','',6,'','','']]
# A = [[5,'', 4, '','',3,'','',''], ['',6,3,4,'','','','',''], ['',8,'',1,'','',3,'',4], ['',5,'','','','',6,'',''], ['',3,6,2,'',1,9,5,''], ['','',2,'','','','',4,''],[7,'',5,'','',9,'',3,''],['','','','','',7,4,9, ''],['','','',5,'','',1,'',6]]
# "World's hardest sudoku puzzle"
A = [['','', 7, '','','',3,'',''], ['',4,'','','','','','',7], [3,'','','','','','',1,''], [6,'','','','',4,'','',''],  ['',1,'','',8,'','','',2],['','',5,3,'','',9,'',''],['','',9,6,'','',5,'',''], ['', 3, '', '',2,'', '','',8], [1,'','','','',7,'',9,'']]

Prettify(A)
start_time = time.time()
PossibleVals = possibleval_maker(A) 
Solution = SudokuDFS(A,PossibleVals)[1]
print("--- %s seconds ---" % (time.time() - start_time))
print(solution)








