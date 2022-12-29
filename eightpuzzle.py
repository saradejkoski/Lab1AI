

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




