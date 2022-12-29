

# Solves a randomized 8-puzzle using A* algorithm with plug-in heuristics

import random

# from functions import hamming_h, manhattan_h

# define start state that is later overwritten with the random generated puzzle, (used to check if solvable)
start_state = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]


def index(item, seq):
    """Helper function that returns -1 for non-found index value of a seq"""
    if item in seq:
        return seq.index(item)
    else:
        return -1


class EightPuzzle:

    def __init__(self):
        # heuristic value
        self.heuristic_val = 0
        # search depth of current instance
        self.depth = 0
        # parent node in search path
        self.parent = None
        self.adj_matrix = []
        for i in range(3):
            self.adj_matrix.append(goal_state[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    def clone(self):
        p = EightPuzzle()
        for i in range(3):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    def get_legal_moves(self):
        # Returns list of tuples with which the free space can be swapped
        # get row and column of the empty piece
        row, col = self.find(0)
        empty = []

        # find which pieces can move there
        if row > 0:
            empty.append((row - 1, col))
        if col > 0:
            empty.append((row, col - 1))
        if row < 2:
            empty.append((row + 1, col))
        if col < 2:
            empty.append((row, col + 1))

        return empty

    def generate_moves(self):
        free = self.get_legal_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self.clone()
            p.swap(a, b)
            p.depth = self.depth + 1
            p.parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    def create_solution_path(self, path):
        if self.parent is None:
            return path
        else:
            path.append(self)
            return self.parent.create_solution_path(path)

    def solve_a_star(self, h):
        """Performs A* search for goal state.
        h(puzzle) - heuristic function, returns an integer
        """

        def is_solved(puzzle):
            return puzzle.adj_matrix == goal_state

        open_l = [self]
        closed_l = []
        move_count = 0
        while len(open_l) > 0:
            x = open_l.pop(0)
            move_count += 1
            if is_solved(x):
                if len(closed_l) > 0:
                    return x.create_solution_path([]), move_count
                else:
                    return [x]

            succ = x.generate_moves()
            # idx_open = idx_closed = -1
            for move in succ:
                # have we already seen this node?
                idx_open = index(move, open_l)
                idx_closed = index(move, closed_l)
                h_val = h(move)
                f_val = h_val + move.depth

                if idx_closed == -1 and idx_open == -1:
                    move.heuristic_val = h_val
                    open_l.append(move)
                elif idx_open > -1:
                    copy = open_l[idx_open]
                    if f_val < copy.heuristic_val + copy.depth:
                        # copy move's values over existing
                        copy.heuristic_val = h_val
                        copy.parent = move.parent
                        copy.depth = move.depth
                elif idx_closed > -1:
                    copy = closed_l[idx_closed]
                    if f_val < copy.heuristic_val + copy.depth:
                        move.heuristic_val = h_val
                        closed_l.remove(copy)
                        open_l.append(move)

            closed_l.append(x)
            open_l = sorted(open_l, key=lambda p: p.heuristic_val + p.depth)

        # if finished state not found, return failure
        return [], 0

    def shuffle(self, step_count):
        for i in range(step_count):
            row, col = self.find(0)
            empty = self.get_legal_moves()
            target = random.choice(empty)
            self.swap((row, col), target)
            _, col = target

    def find(self, value):
        """returns the row, col coordinates of the specified value
           in the graph"""
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    def peek(self, row, col):
        # returns the value at the specified row and column
        return self.adj_matrix[row][col]

    def poke(self, row, col, value):
        # sets the value at the specified row and column
        self.adj_matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        # swap values at the specified coordinates
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)


"""

---


Functions.py



---


"""


def heuristic(puzzle, item_total_calc, total_calc):
    """
    Heuristic template that provides the current and target position for each number and the
    total function.

    Parameters:
    puzzle - the puzzle
    item_total_calc - takes 4 parameters: current row, target row, current col, target col.
    Returns int.
    total_calc - takes 1 parameter, the sum of item_total_calc over all entries, and returns int.
    This is the value of the heuristic function
    """
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.peek(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            # account for 0 as blank
            if target_row < 0:
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)


def is_puzzle_solvable(array):
    inv_count = 0
    empty_puzzle = []

    for i in array:
        empty_puzzle += i

    for i in range(8):
        for j in range(i + 1, 9):
            if empty_puzzle[j] and empty_puzzle[i] and empty_puzzle[i] > empty_puzzle[j]:
                inv_count += 1

    # return if inversion count is even.
    return inv_count % 2 == 0


# some heuristic functions, the best being the standard manhattan distance in this case, as it comes
# closest to maximizing the estimated distance while still being admissible.

def manhattan_h(puzzle):
    return heuristic(puzzle,
                     lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                     lambda t: t)


def hamming(row, target_row, column, target_column):
    if row != target_row or column != target_column:
        return 1
    return 0


def hamming_h(puzzle):
    return heuristic(puzzle,
                     hamming,
                     lambda t: t)


"""Test whether random generated puzzle is solvable or not: (in our case it is almost always solvable, due to the defined function)"""


def main():
    p = EightPuzzle()
    p.shuffle(12)
    print(p)
    p = start_state

    # path, count = p.solve_a_star(manhattan_h)
    # path.reverse()
    # for i in path:
    # print(i)

    # print(goal_state)

    if is_puzzle_solvable(start_state):
        print("Solvable")
    else:
        print("Not Solvable")


if __name__ == "__main__":
    main()

"""

---


main.py


---



"""

import time


# ---------------------------------------------------------------
# Defines menu that is printed for the user to choose from
# ---------------------------------------------------------------

# from Eight_puzzle.eight_puzzle import EightPuzzle, start_state, goal_state
# from functions import manhattan_h, hamming_h, is_puzzle_solvable


def menu():
    print("---------------------------------------------------------------------------------")
    print("Eight Puzzle Implementation using Heuristic Search: ")
    print("---------------------------------------------------------------------------------")
    print("Choose a number from 1 to 7:")
    print("1. Display Random Puzzle: ")
    print("2. Display Goal State ")
    print("3. Check if puzzle is solvable:")
    print("4. Solve the puzzle using the Manhattan Heuristic:")
    print("5. Solve the puzzle using the Hamming Heuristic:")
    print("6. Print the Results of both Heuristics:  ")
    print("7. Quit. ")
    print("---------------------------------------------------------------------------------")


def main():
    p = EightPuzzle()

    def print_random_puzzle():
        p.shuffle(20)
        print(p)

    def check_if_solvable():
        p = start_state

        if is_puzzle_solvable(start_state):
            print("Solvable")
        else:
            print("Not Solvable")

    def solve_puzzle_with_manhattan():
        start_time = time.time()
        print("---------------------------------------------------------------------------------")
        path, count = p.solve_a_star(manhattan_h)
        print("Solved with Manhattan distance exploring", count, "states")
        print("--- %s milliseconds for MANHATTAN ---" % ((time.time() - start_time) * 1000))
        print("---------------------------------------------------------------------------------")

    def solve_puzzle_with_hamming():
        start_time = time.time()
        print("---------------------------------------------------------------------------------")
        path, count = p.solve_a_star(hamming_h)
        print("Solved with Hamming distance exploring", count, "states")
        print("--- %s milliseconds for HAMMING ---" % ((time.time() - start_time) * 1000))
        print("---------------------------------------------------------------------------------")

    def compare_results():
        print("---------------------------------------------------------------------------------")
        # Measure Manhattan Complexity:
        start_time = time.time()
        path, count = p.solve_a_star(manhattan_h)
        print("--- %s milliseconds for MANHATTAN ---" % ((time.time() - start_time) * 1000))
        print("Solved with Manhattan distance exploring", count, "states")
        print("---------------------------------------------------------------------------------")
        # Measure Hamming Complexity:
        start_time = time.time()
        path, count = p.solve_a_star(hamming_h)
        print("--- %s milliseconds for HAMMING ---" % ((time.time() - start_time) * 1000))
        print("Solved with Hamming distance exploring", count, "states")
        print("---------------------------------------------------------------------------------")

        # states: count all the possible nodes that are generated to solve the puzzle

    menu()

    choice = (input("Enter an integer between 1-7: "))

    run = True
    while run:
        if choice == "1":
            print_random_puzzle()
            menu()
            choice = (input("Enter an integer between 1-7: "))
        elif choice == "2":
            print(goal_state)
            menu()
            choice = (input("Enter an integer between 1-7: "))
        elif choice == "3":
            check_if_solvable()
            menu()
            choice = (input("Enter an integer between 1-7: "))
        elif choice == "4":
            print("Solved with Manhattan:")
            solve_puzzle_with_manhattan()
            menu()
            choice = (input("Enter an integer between 1-7: "))
        elif choice == "5":
            print("Solved with Hamming:")
            solve_puzzle_with_hamming()
            menu()
            choice = (input("Enter an integer between 1-7: "))
        elif choice == "6":
            compare_results()
            menu()
            choice = (input("Enter an integer between 1-7: "))
        elif choice == "7":
            print("Quit Puzzle")
            run = False
        else:
            print("Invalid Option! ")
            choice = (input("Enter an integer between 1-7: "))


if __name__ == "__main__":
    main()
