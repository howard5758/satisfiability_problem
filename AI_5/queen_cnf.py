from SAT import SAT

def write_queen_cnf(q):

	var = []
	for i in range(0, q):
		for j in range(1, q + 1):
			var.append(q * i + j)

	print(var)
	f = open(str(q) + "_queens.cnf", "w")

	clause = ""

	for i in range(1, q + 1):
		
		for j in range(1, q + 1):
			f.write(str(q * ((i - 1)%q) + j) + " ")

		for ii in range(1, q + 1):
			for jj in range(1, q +1):
				if jj > ii:
					f.write("\n" + "-" + str(q * ((i - 1)%q) + ii) + " -" + str(q * ((i - 1)%q) + jj))

		f.write("\n")	

	for i in range(1, q + 1):
		
		for j in range(1, q + 1):
			f.write(str(q * ((j - 1)%q) + i) + " ")

		for ii in range(1, q + 1):
			for jj in range(1, q +1):
				if jj > ii:
					f.write("\n" + "-" + str(q * ((ii - 1)%q) + i) + " -" + str(q * ((jj - 1)%q) + i))

		f.write("\n")

	for i in range(1, q + 1):

		for j in range(1, q +1):

			for k in range(max(i, j) + 1, q + 1):
				f.write("-" + str(q * ((i - 1)%q) + j) + " -" + str(q * (((i + 1 + q - k) - 1)%q) + j + 1 + q - k) + "\n")
		
	for k in range(2, 2 * q + 1):

		temp = []
		for i in range(1, q + 1):
			for j in range(1, q +1):
				if i + j == k:
					temp.append((i, j))

		for i in range(0, len(temp)):
			for j in range(i, len(temp)):
				if j > i:
					f.write("-" + str(q * ((temp[i][0] - 1)%q) + temp[i][1]) + " -" + str(q * ((temp[j][0] - 1)%q) + temp[j][1]) + "\n")
		
def print_sol(sol_filename, q):

	f = open(sol_filename, "r")
	sol = []
	for line in f:
		sol.append(int(line[0 : len(line) - 1]))
	
	for i in range(1, q * q + 1):
		if i in sol:
			print("Q ", end="")
		else:
			print("# ", end="")
		if i%q == 0:
			print("\n", end="")


if __name__ == "__main__":

	q = 15
	
	write_queen_cnf(q)
	sat = SAT(str(q) + "_queens" + ".cnf")
	sol_filename = str(q) + "_queens" + ".sol"
	result = sat.walksat()

	if result:
		sat.write_solution(sol_filename)
		print_sol(sol_filename, q)

