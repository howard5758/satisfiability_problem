from display import display_sudoku_solution
import random, sys
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    puzzle_name = str("all_cells")
    sol_filename = puzzle_name + ".sol"

    sat = SAT("all_cells.cnf")

    result = sat.walksat()

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
