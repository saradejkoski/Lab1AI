import time

from eightpuzzle import EightPuzzle, start_state, goal_state
from functions import is_puzzle_solvable, manhattan_h, hamming_h


# ---------------------------------------------------------------
# Defines menu that is printed for the user to choose from
# ---------------------------------------------------------------
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

    def print_random_puzzle():  # prints out random puzzle for 1.
        p.shuffle(20)
        print(p)

    def check_if_solvable():  # checks if the puzzle is solvable
        p = start_state

        if is_puzzle_solvable(start_state):
            print("Solvable")
        else:
            print("Not Solvable")

    def solve_puzzle_with_manhattan():  # solving puzzle with manhattan and the time it needs for that
        start_time = time.time()
        path, count = p.solve_a_star(manhattan_h)
        print("Solved with Manhattan distance exploring", count, "states")
        print("%s milliseconds for MANHATTAN " % ((time.time() - start_time) * 1000))

    def solve_puzzle_with_hamming():  # solving puzzle with hamming and the time it needs for that
        start_time = time.time()
        path, count = p.solve_a_star(hamming_h)
        print("Solved with Hamming distance exploring", count, "states")
        print("%s milliseconds for HAMMING" % ((time.time() - start_time) * 1000))

    def compare_results():  # comparing the results of the two methods manhattan and hamming
        print("---------------------------------------------------------------------------------")
        # Measure Manhattan Complexity:
        start_time = time.time()
        path, count = p.solve_a_star(manhattan_h)
        print("%s milliseconds for MANHATTAN" % ((time.time() - start_time) * 1000))
        print("Solved with Manhattan distance exploring", count, "states")
        print("---------------------------------------------------------------------------------")
        # Measure Hamming Complexity:
        start_time = time.time()
        path, count = p.solve_a_star(hamming_h)
        print("%s milliseconds for HAMMING" % ((time.time() - start_time) * 1000))
        print("Solved with Hamming distance exploring", count, "states")

        # states: count all the possible nodes that are generated to solve the puzzle

    menu()

    choice = (input("Enter an integer between 1-7: "))   # method to print when entering a specific number

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
            print("Manhattan:")
            solve_puzzle_with_manhattan()
            menu()
            choice = (input("Enter an integer between 1-7: "))
        elif choice == "5":
            print("Hamming:")
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
