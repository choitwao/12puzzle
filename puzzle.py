from cli import Cli
from solver import Solver
import os


def validate_state(init_state, goal_state, width, height):
    print('Initial State: ' + str(init_state))
    print('Goal State: ' + str(goal_state))
    print('Puzzle Size: ' + str(width) + ' by ' + str(height))
    print('Validating the puzzle configuration......')
    validation = 0
    # checking if both init_state and goal_state has identical numbers of tile and fit the defined width and height
    if len(init_state) == len(goal_state) == int(height) * int(width):
        validation += 1
        print('Matrix size validation is good.')
    # checking if both init_state and goal_state have the right numbers (i.e. for 4x3 puzzle should have 0~11)
    number = 0
    while number < int(height) * int(width):
        if number in init_state and number in goal_state:
            number += 1
    if number == int(height) * int(width):
        validation += 1
        print('Tile number validation is good.')
    return validation == 2


def convert_state_to_int(state):
    int_state = []
    for item in state.split(','):
        int_state.append(int(item))
    return int_state


if __name__ == '__main__':

    args = Cli.create_parser().parse_args()
    print('\n\n-----------------------------------------------------------------------')
    # init solver with validated input
    init_state = convert_state_to_int(args.init_state)
    goal_state = convert_state_to_int(args.goal_state)
    width = int(args.width)
    height = int(args.height)
    if validate_state(init_state, goal_state, width, height):
        s = Solver(init_state, goal_state, width)
        # use DFS
        if args.subparser_name == 'DFS':
            s.search_DFS()
        else:
            # check if h1 and h2 are selected. Only one heuristic function can be selected.
            heuristic_type = None
            if args.h1 is True and args.h2 is True:
                print('You can only select one of the heuristic functions.')
                os._exit(1)
            elif args.h1 is False and args.h2 is False:
                print('You must select one heuristic function.')
                os._exit(1)
            else:
                heuristic_type = 'h1' if args.h1 else 'h2'
            # use BFS
            if args.subparser_name == 'BFS':
                s.search_BFS(heuristic_type)
            # use A*
            if args.subparser_name == 'ASTAR':
                s.search_Astar(heuristic_type)
    else:
        print('Invalid puzzle configuration.')




