import sys
import time
import itertools
import csp
from csp import CSP
import numpy
import ast

""" We are using python 3 """

class Kakuro(CSP):
	def __init__(self, rows, columns, vars_result, black_boxes):
		"""Constructor of Kakuro instance"""
		self.rows 			= rows
		self.columns 		= columns
		self.vars_result 	= vars_result
		self.black_vars 	= black_boxes
		#print(vars_result)
		#Take variables 
		variables = []
		for row in range(rows):
			for column in range(columns):
				var = "X" + str(row) + str(column)
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
			#print("var == " +var)
			for row in range(rows):
				for column in range(columns):
					neighbor = "X" + str(row) + str(column)
					if (neighbor != var) and (neighbor not in black_boxes) and (var_row == row or var_column == column):
						for constraint in vars_result:
							if var in constraint[0] and neighbor in constraint[0]:
								neighbors[var].append(neighbor)
								break
		"""
		for val in variables:
			print("neighbors[val]")
			print(neighbors[val])
		"""
		#create a CSP problem
		CSP.__init__(self, variables, domains, neighbors, self.constraints)

	def constraints(self, A, a, B, b):
		if a == b:				#variables in the same constraint can't take the same
			return False

		noValueCounter 	= 0
		values 			= []
		values.append(a)
		values.append(b)

		for list_item in self.vars_result:	#for every constraint in list of constraints
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

					if(noValueCounter > 0):		#if there are values for the constraint that are empty
						sum = 0
						for value in values:
							sum += value
						if sum <= result - noValueCounter:		#we have just to check if sum <= result
							return True			#because if sum > result then we know for sure that the constraint
												#is not satisfied
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
		print("You didn't give the correct arguments! Try: python kakuro.py puzzle_file")
	else:
		#puzzle_file = open("./Puzzles/" + sys.argv[1],'r')
		puzzle_file = open(sys.argv[1],'r')
		lines = puzzle_file.readlines()
		puzzle_file.close()

		rows 	= int(lines[0])
		columns = int(lines[1])

		vars_result = []
		temp_black 	= []

		for i in range(2, len(lines)):
			x = ast.literal_eval(lines[i])
			if (len(x) == 2 and type(x[0]) is list):
				vars_result.append(x)
			else:
				temp_black.append(x)
		
		black_boxes = [item for sublist in temp_black for item in sublist]

		#print("vars_result")
		#print(vars_result)

		#print("black_boxes")
		#print(black_boxes)
		#current_milli_time = lambda: int(round(time.time() * 1000))
		
		kakuro 		= Kakuro(rows,columns,vars_result,black_boxes)
		start 		= time.time()
		result_BT 	= csp.backtracking_search(kakuro)
		end 		= time.time()
		print("Solving kakuro puzzle with BT in %lf seconds and %d assignments.\n" % ((end - start), kakuro.nassigns))
		
		kakuro 			= Kakuro(rows,columns,vars_result,black_boxes)
		start 			= time.time()
		result_BT_LCV	= csp.backtracking_search(kakuro,order_domain_values=csp.lcv)
		end 			= time.time()
		print("Solving kakuro puzzle with BT+LCV in %lf seconds and %d assignments.\n" % ((end - start), kakuro.nassigns))
		

		kakuro 		= Kakuro(rows,columns,vars_result,black_boxes)
		start 		= time.time()
		result_FC 	= csp.backtracking_search(kakuro, inference=csp.forward_checking)
		end 		= time.time()
		print("Solving kakuro puzzle with FC in %lf seconds with %d assignments.\n" % ((end - start), kakuro.nassigns))
		
		kakuro 			= Kakuro(rows,columns,vars_result,black_boxes)
		start 			= time.time()
		result_FC_MRV 	= csp.backtracking_search(kakuro, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
		end 			= time.time()
		print("Solving kakuro puzzle with FC+MRV in %lf seconds and %d assignments.\n" % ((end - start), kakuro.nassigns))
		"""
		kakuro 			= Kakuro(rows,columns,vars_result,black_boxes)
		start 			= time.time()
		result_FC_LCV 	= csp.backtracking_search(kakuro, order_domain_values=csp.lcv, inference=csp.forward_checking)
		end 			= time.time()
		print("Solving kakuro puzzle with FC+LCV in %lf seconds and %d assignments.\n" % ((end - start), kakuro.nassigns))
		"""
		kakuro 				= Kakuro(rows,columns,vars_result,black_boxes)
		start 				= time.time()
		result_FC_MRV_LCV 	= csp.backtracking_search(kakuro, order_domain_values=csp.lcv, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
		end 				= time.time()
		print("Solving kakuro puzzle with FC+MRV+LCV in %lf seconds and %d assignments.\n" % ((end - start), kakuro.nassigns))

		kakuro 		= Kakuro(rows,columns,vars_result,black_boxes)
		start 		= time.time()
		result_MAC 	= csp.backtracking_search(kakuro,inference=csp.mac)
		end 		= time.time()
		print("Solving kakuro puzzle with MAC in %lf seconds with %d assignments.\n" % ((end - start), kakuro.nassigns))
		
		"""
		kakuro 					= Kakuro(rows,columns,vars_result,black_boxes)
		start 					= time.time()
		result_min_conflicts 	= csp.min_conflicts(kakuro)
		end 					= time.time()
		print("Solving kakuro puzzle with min_conflicts in %lf seconds with %d assignments.\n" % ((end - start), kakuro.nassigns))
		"""
		print("~~~~~~Solution~~~~~~")
		for row in range(rows):
			for column in range(columns):
				if (result_FC != None):
					for (var, val) in result_FC.items():
						if var == "X" + str(row) + str(column):
							print("%s = %d" % (var, val), end = "  ")
				else:
					print("Something went really wrong!! Time for debug..")
			print("")