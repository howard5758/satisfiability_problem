# Author: Ping-Jung Liu
# Date: October 25th 2017
# COSC 76 Assignment 5: Sudoku with SAT
# Acknowledgement: Professor Devin Balkom for providing structues and suggestions 

import random, sys

class SAT:

	def __init__(self, f):
		# filename
		self.f = f
		# solution dictionary
		self.sol = {}
		# list of variables
		self.X = []
		# list of clauses
		self.clause = []
		# threshold to determine random selection or sat
		self.h = 0.9
	
	def gsat(self):

		f = open(self.f, "r")

		# get the variables
		for line in f:
			
			self.clause.append(line.split())

			for word in line.split():
				if not word[0] == "-":
					self.X.append(word)

		self.X = list(set(self.X))
		
		# generate the list of clauses
		for clause in self.clause:
			for i in range(0, len(clause)):

				sign = 1
				single = clause[i]
				if single[0] == "-":
					single = single[1:]
					sign = -1
				clause[i] = sign * (self.X.index(single) + 1)
		
		f.close()

		# initialize solution to be all False
		for i in range(0, len(self.X)):
			self.sol[i + 1] = -1

		# counter for testing
		counter = 0
		# keep search until solution found
		while not self.is_solution():

			counter = counter + 1

			# if a random int between 0 to 1 is greater than h
			# randomly flip a variable
			if random.randint(1, 100)/100 > self.h:

				ind = random.randint(1, len(self.X))
				self.sol[ind] = -1 * self.sol[ind]

			# if not, perform gsat
			else:

				# If key var is flipped, value clauses will be satisfied
				var_match = {}
				max_count = 0
				# list of variable to choose from
				pool = []

				for var in self.sol:
					# get the number of clause satisfied if var is flipped
					count = self.get_match(var)
					var_match[var] = count
					# update highest number of clause satisfied
					if count > max_count:
						max_count = count

				print(max_count)
				# get the pool of variable to choose from
				for var in var_match:
					if var_match[var] == max_count:
						pool.append(var)

				varr = random.choice(pool)

				self.sol[varr] = -1 * self.sol[varr]
				
				#if counter == 5000:
				#	break
	
		return True

	def walksat(self):

		f = open(self.f, "r")

		# get the variables
		for line in f:
			
			self.clause.append(line.split())

			for word in line.split():
				if not word[0] == "-":
					self.X.append(word)

		self.X = list(set(self.X))
		
		# generate the list of clauses
		for clause in self.clause:
			for i in range(0, len(clause)):

				sign = 1
				single = clause[i]
				if single[0] == "-":
					single = single[1:]
					sign = -1
				clause[i] = sign * (self.X.index(single) + 1)
		
		f.close()

		# initialize solution to be all False
		for i in range(0, len(self.X)):
			self.sol[i + 1] = -1

		# counter for testing
		counter = 0
		# keep search until solution found
		while not self.is_solution():

			counter = counter + 1

			# if a random int between 0 to 1 is greater than h
			# randomly flip a variable
			if random.randint(1, 100)/100 > self.h:

				ind = random.randint(1, len(self.X))

				if not [ind * self.sol[ind]] in self.clause:
					self.sol[ind] = -1 * self.sol[ind]

			# if not, perform walksat
			else:

				# same as gsat
				var_match = {}
				max_count = 0
				pool = []
				
				# randomly choose a unsatisfied clause
				cand = self.candidate_clause()
				clauses = random.choice(cand)
				# list of variables in this clause
				rand_clause = []
				# get the variables in this clause
				for i in range(0, len(clauses)):
					rand_clause.append(abs(clauses[i]))
				
				# every 2000 iterations, perform gsat in hopes of escaping local minimum
				if counter % 2000 == 0:
					var_candidate = list(self.sol)
				else:
					var_candidate = rand_clause

				for var in var_candidate:
					# get the number of clause satisfied if var is flipped
					count = self.get_match(var)
					var_match[var] = count
					# update highest number of clause satisfied
					if count > max_count:
						max_count = count

				print(max_count)
				# get the pool of variable to choose from
				for var in var_match:
					if var_match[var] == max_count:
						pool.append(var)

				varr = random.choice(pool)
				
				if not [varr * self.sol[varr]] in self.clause:
					self.sol[varr] = -1 * self.sol[varr]
				
				#if counter == 5000:
				#	break
		print(str(counter) + "iterations")
		return True
		
	# get a list of all unsatisfied clauses
	def candidate_clause(self):

		cand = []

		for clause in self.clause:
			flag = False
			for atom in clause:
				varr = abs(atom)
				if varr * self.sol[varr] == atom:
					flag = True
					break
			if not flag:
				cand.append(clause)

		return cand

	# calculate the number of satisfied clauses if var is flipped
	def get_match(self, var):

		count = 0

		for clause in self.clause:
			for atom in clause:
				varr = abs(atom)
				if varr == var:
					if varr * self.sol[varr] * -1 == atom:
						count = count + 1
						break
				else:
					if varr * self.sol[varr] == atom:
						count = count + 1
						break
		return count

	# check if current assignment is the solution
	def is_solution(self):

		for clause in self.clause:
			flag = False

			for atom in clause:
				varr = abs(atom)
				if varr * self.sol[varr] == atom:
					flag = True
					break

			if not flag:
				return False

		return True

	def write_solution(self, sol_name):
		
		f = open(sol_name, "w")
		for var in self.sol:
			if self.sol[var] == 1:
				f.write(str(self.X[var -1]) + "\n")

if __name__ == "__main__":

	test = SAT("all_cells.cnf")
	test.gsat()
	test.write_solution("test_sol.cnf")


