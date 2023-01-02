from eightpuzzle import EightPuzzle, start_state


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


def is_puzzle_solvable(array):  # checks if puzzle is solvable, uses inversion count
    inv_count = 0
    empty_puzzle = []

    for i in array:
        empty_puzzle += i

    for i in range(8):
        for j in range(i + 1, 9):
            if empty_puzzle[j] and empty_puzzle[i] and empty_puzzle[i] > empty_puzzle[j]:
                inv_count += 1

    # return if inversion count is even. --> solvable, if inversion count is uneven --> not solvable
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

    if is_puzzle_solvable(start_state):
        print("Solvable")
    else:
        print("Not Solvable")


if __name__ == "__main__":
    main()
