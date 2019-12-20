import sys
import time
import itertools
import csp
from csp import CSP
import numpy
import ast

""" We are using python 3 """

def add(numbers):
	sum = 0
	for n in numbers:
		sum += n
	return sum
	
class Kakuro(CSP):

	def __init__(self, rows, columns, vars_result, black_boxes):
		"""Constructor of Kakuro instance"""
		self.rows 			= rows
		self.columns 		= columns
		self.vars_result 	= vars_result
		self.black_vars 	= black_boxes
		
		#Take variables 
		variables = []
		for row in range(rows):
			for column in range(columns):
				var = "X%d%d" % (row,column)
				if (var not in black_boxes):
					variables.append(var)		
		#print("variables")
		#print(variables)
		domains = { }
		neighbors = { }
		#fill domains and neighbors 
		for var in variables:
			var_row = int(var[1])
			var_column = int(var[2])
			domains[var] = [n + 1 for n in range(9)]
			neighbors[var] = [ ]
			for row in range(rows):
				for column in range(columns):
					neighbor = "X%d%d" % (row,column)
					if (neighbor != var) and (neighbor not in black_boxes) and (var_row == row or var_column == column):
						neighbors[var].append(neighbor)
		"""
		for val in variables:
			print("neighbors[val]")
			print(neighbors[val])
		"""
		#create a CSP problem
		CSP.__init__(self, variables, domains, neighbors, self.constraints)

	def constraints(self, A, a, B, b):
		
		if (A[1] == B[1] or A[2] == B[2]):
			flag = 0
			for l in self.vars_result:
				if ((A in l[0]) and (B in l[0])):
					flag = 1
			if a == b and flag == 1:
				return False
		
		noValueCounter 	= 0
		values 			= []
		values.append(a)
		values.append(b)

		for list_item in self.vars_result:
			variables 	= list_item[0]
			result 		= list_item[1]
			
			#if we find the constrain that the two variables exist together
			if A in variables and B in variables:
				if len(variables) == 2: #if the constraint has only these two variables
					if a+b == result:
						return True
					else:
						return False
				else:
					for var in variables:
						if var == A:
							continue
						elif var == B:
							continue
						else:
							if self.curr_domains != None and len(self.curr_domains[var]) == 1:
								values.append(*self.curr_domains[var])
							else:
								noValueCounter += 1
				
				if(noValueCounter > 0):
					sum = 0
					for value in values:
						sum += value
					if sum <= result:
						return True
					else:
						return False
				else:
					sum = 0
					for value in values:
						sum += value
					if sum == result:
						return True
					else:
						return False




if __name__ == '__main__':

	if len(sys.argv) != 2:
		print("You didn't give the correct arguments! Try python kakuro.py puzzle_file")
	else:
		puzzle_file = open("./Puzzles/" + sys.argv[1],'r')
		lines = puzzle_file.readlines()
		puzzle_file.close()

		rows = int(lines[0])
		columns = int(lines[1])

		vars_result = []
		temp_black = []

		for i in range(2, len(lines)):
			x = ast.literal_eval(lines[i])
			if (len(x) == 2):
				vars_result.append(x)
			else:
				temp_black.append(x)
		
		black_boxes = [item for sublist in temp_black for item in sublist]

		#print("vars_result")
		#print(vars_result)

		#print("black_boxes")
		#print(black_boxes)

		print("-->BT")
		BT = Kakuro(rows,columns,vars_result,black_boxes)
		start = int(round(time.time()*1000))
		result_BT = csp.backtracking_search(BT)
		end = int(round(time.time()*1000))
		print("Solved with BT in %d mseconds with %d assignments.\n" % (end - start, BT.nassigns))
		

		print("-->FC")
		FC = Kakuro(rows,columns,vars_result,black_boxes)
		start = int(round(time.time()*1000))
		result_FC = csp.backtracking_search(FC, inference=csp.forward_checking)
		end = int(round(time.time()*1000))
		print("Solved with FC in %d mseconds with %d assignments.\n" % (end - start, FC.nassigns))

		print("-->FC+MRV")
		FC_MRV = Kakuro(rows,columns,vars_result,black_boxes)
		start = int(round(time.time()*1000))
		result_FCMRV = csp.backtracking_search(FC_MRV, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
		end = int(round(time.time()*1000))
		print("Solved with FC+MRV in %d mseconds with %d assignments.\n" % (end - start, FC_MRV.nassigns))

		print("-->MAC")
		MAC = Kakuro(rows,columns,vars_result,black_boxes)
		start = int(round(time.time()*1000))
		result_MAC = csp.backtracking_search(MAC, inference=csp.mac)
		end = int(round(time.time()*1000))
		print("Solved with MAC in %d mseconds with %d assignments.\n" % (end - start, MAC.nassigns))

		
		print("\nSollution (--> Variable = Values):\n")
		for i in range(rows):
			for j in range(columns):
				if (result_BT.items()!=None):
					for (var, val) in result_BT.items():
						if var == "X%d%d" % (i, j):
							print("%s = %d" % (var, val), end = "  ")
			print("")