# -*- coding:utf8 -*-
"""
solver.py contains all the implementation of heuristic search algorithms
"""
from queue import PriorityQueue, Queue
from state import State
import time
import copy


class Solver:

    def __init__(self, init_state, goal_state, width):
        self.__init_state = self.__convert_state__(init_state, width)
        self.__goal_state = self.__convert_state__(goal_state, width)
        self.__path = []
        self.__steps = 0

    # Iterative Deepening Depth-First Search
    # I use IDDFS as the default algorithm for DFS search since DFS doesn't yield good result.
    # IDDFS is built on DFS
    def search_IDDFS(self, limit, iteration):
        current_limit = 0
        # Iteratively increase the depth limit and run DFS
        while current_limit < limit:
            self.search_DFS(limit=current_limit, iteration=iteration)
            current_limit += 1
            if len(self.__path) > 0:
                break

    # Depth-First Search
    # `iteration` defined the maximum steps the DFS can go
    # `limit` is set to None by default for pure DFS. Should set to INT for IDDFS.
    def search_DFS(self, iteration, limit=None):
        print('\nStarting heuristic search using DFS......')
        tic = time.clock()
        # create open_list (stack) for storing non-explored nodes (node object)
        open_list = []
        # plain_open_list is to save the puzzle only without any info about the tree (list)
        # this gives constant complexity when checking if a new child is in open_list
        plain_open_list = []
        # create close_list for storing explored nodes (list)
        close_list = []
        # put initial state (node object) in the open_list and plain_open_list
        init_state = State(self.__init_state, self.__goal_state, 0)
        open_list.append(init_state)
        plain_open_list.append(self.__init_state)
        # start searching
        while len(open_list) > 0 and self.__steps < iteration:
            current_state = open_list.pop()
            plain_open_list.remove(current_state.get_state())
            # check if goal state is reached
            if current_state.get_state() == self.__goal_state:
                self.__create_path__(current_state)
                tic = time.clock() - tic
                self.__steps += 1
                break
            # if reach the limit (for iterative deepening)
            elif limit is not None and current_state.get_depth() + 1 > limit:
                self.__steps += 1
                continue
            # search for children
            else:
                # find all the possible moves based on current state
                for state in self.__find_possible_states__(current_state.get_state()):
                    # check if this state is in open_list or close_list
                    if state not in close_list and state not in plain_open_list:
                        # create state node, push to open_list
                        new_state = State(state, self.__goal_state, current_state.get_depth() + 1, current_state)
                        open_list.append(new_state)
                        plain_open_list.append(state)
                # add the current state to close_list
                close_list.append(current_state.get_state())
                self.__steps += 1
        # if no solution is found
        if len(self.__path) == 0:
            print('This puzzle is unsolvable.' if limit is None else 'This puzzle is unsolvable with depth limit ' + str(limit))
        # if solution is found, print and save the result in a file
        else:
            self.__save_result__('puzzleDFS', tic)

    # Breadth-First Search
    # `heuristic_type` takes either `h1` or `h2`
    # `h1` stands for hamming distance, and `h2` is the sum of permutation
    # `iteration` is the maximum step of the search
    def search_BFS(self, heuristic_type, iteration):
        print('\nStarting heuristic search using BFS with ' + heuristic_type + '......')
        tic = time.clock()
        # create open_list (queue) for storing non-explored nodes (node object)
        open_list = Queue()
        # plain_open_list is to save the puzzle only without any info about the tree (list)
        # this gives constant complexity when checking if a new child is in open_list
        plain_open_list = []
        # create close_list for storing explored nodes (list)
        close_list = []
        # put initial state (node object) in the open_list and plain_open_list
        init_state = State(self.__init_state, self.__goal_state, 0)
        open_list.put(init_state)
        plain_open_list.append(self.__init_state)
        # start searching
        while open_list.qsize() and self.__steps < iteration:
            current_state = open_list.get()
            plain_open_list.remove(current_state.get_state())
            # check if goal state is reached
            if current_state.get_state() == self.__goal_state:
                self.__create_path__(current_state)
                tic = time.clock() - tic
                self.__steps += 1
                break
            # search for children
            else:
                new_state_list = []
                # find all the possible moves based on current state
                for state in self.__find_possible_states__(current_state.get_state()):
                    # check if this state is in open_list or close_list
                    if state not in close_list and state not in plain_open_list:
                        # create state node, add to a temp list
                        new_state = State(state, self.__goal_state, current_state.get_depth() + 1, current_state)
                        new_state_list.append(new_state)
                        plain_open_list.append(state)
                # if hamming distance, sort the temp list based on f(s) = g(s) + h1(s)
                if heuristic_type == 'h1':
                    new_state_list = sorted(new_state_list, key=lambda x: x.get_h1())
                # if sum of permutation, sort the temp list based on f(s) = g(s) + h2(s)
                else:
                    new_state_list = sorted(new_state_list, key=lambda x: x.get_h2())
                # add the state nodes in the temp list to open_list
                for state in new_state_list:
                    open_list.put(state)
                close_list.append(current_state.get_state())
                self.__steps += 1
        # if no solution is found
        if len(self.__path) == 0:
            print('This puzzle is unsolvable.')
        # if solution is found, print and save the result in a file
        else:
            self.__save_result__('puzzleBFS-h1' if heuristic_type is 'h1' else 'puzzleBFS-h2', tic)

    # A* Algorithm Search
    # `heuristic_type` takes either `h1` or `h2`
    # `h1` stands for hamming distance, and `h2` is the sum of permutation
    # `iteration` is the maximum step of the search
    def search_Astar(self, heuristic_type, iteration):
        print('\nStarting heuristic search using A* with ' + heuristic_type + '......')
        tic = time.clock()
        # create open_list (priority queue)for storing non-explored nodes (node object)
        open_list = PriorityQueue()
        # plain_open_list is to save the puzzle only without any info about the tree (list)
        # this gives constant complexity when checking if a new child is in open_list
        plain_open_list = []
        # create close_list for storing explored nodes (list)
        close_list = []
        # put initial state (node object) in the open_list and plain_open_list
        init_state = State(self.__init_state, self.__goal_state, 0)
        open_list.put(init_state)
        plain_open_list.append(self.__init_state)
        # start searching
        while open_list.qsize() and self.__steps < iteration:
            current_state = open_list.get()
            plain_open_list.remove(current_state.get_state())
            # check if goal state is reached
            if current_state.get_state() == self.__goal_state:
                self.__create_path__(current_state)
                tic = time.clock() - tic
                self.__steps += 1
                break
            # search for children
            else:
                # find all the possible moves based on current state
                for state in self.__find_possible_states__(current_state.get_state()):
                    # check if this state is in open_list or close_list
                    if state not in close_list and state not in plain_open_list:
                        # create state node
                        new_state = State(state, self.__goal_state, current_state.get_depth() + 1, current_state)
                        plain_open_list.append(state)
                        # if hamming distance, set f(s) = g(s) + h1(s) as the priority of the node, add to open_list
                        if heuristic_type == 'h1':
                            new_state.get_h1()
                            open_list.put(new_state)
                        # if sum of permutation, set f(s) = g(s) + h1(s) as the priority of the node, add to open_list
                        else:
                            new_state.get_h2()
                            open_list.put(new_state)
                # add the current state to close_list
                close_list.append(current_state.get_state())
                self.__steps += 1
        # if no solution is found
        if len(self.__path) == 0:
            print('This puzzle is unsolvable.')
        # if solution is found, print and save the result in a file
        else:
            self.__save_result__('puzzleAs-h1' if heuristic_type is 'h1' else 'puzzleAs-h2', tic)

    # getter for path
    def get_path(self):
        return self.__path

    # convert a list of puzzle to a new list of lists where the size equals to the height of the puzzle
    # i.e [1,2,3,4,5,6,7,0] ->
    # [[1,2,3,4],[5,6,7,0]] for 4x2
    def __convert_state__(self, state, width):
        converted_state = [state[tile:tile+width] for tile in range(0, len(state), width)]
        return converted_state

    # This method is to find out all the possible moves based on the current state
    # Only returns the state without any info of the search (i.e. h1, h2, depth etc.)
    def __find_possible_states__(self, state):
        next_states = []
        # locate blank 0
        blank_x = -1
        blank_y = -1
        for row_idx, row in enumerate(state):
            if 0 in row:
                blank_x = row_idx
                blank_y = row.index(0)
        # UP > UP –RIGHT > RIGHT > DOWN- RIGHT > DOWN > DOWN –LEFT > LEFT > UP–LEFT
        # (most preferred moves)  > (least preferred moves)
        move_position = [
            {
                'exist': blank_x < len(state) - 1,
                'position': [1, 0]
            },
            {
                'exist': blank_x < len(state) - 1 and blank_y > 0,
                'position': [1, -1]
            },
            {
                'exist': blank_y > 0,
                'position': [0, -1]
            },
            {
                'exist': blank_x > 0 and blank_y > 0,
                'position': [-1, -1]
            },
            {
                'exist': blank_x > 0,
                'position': [-1, 0]
            },
            {
                'exist': blank_x > 0 and blank_y < len(state[0]) - 1,
                'position': [-1, 1]
            },
            {
                'exist': blank_y < len(state[0]) - 1,
                'position': [0, 1]
            },
            {
                'exist': blank_x < len(state) - 1 and blank_y < len(state[0]) - 1,
                'position': [1, 1]
            }
        ]
        # generate states of possible moves
        for move in move_position:
            if move['exist']:
                new_state = copy.deepcopy(state)
                new_state[blank_x][blank_y] = state[blank_x + move['position'][0]][blank_y + move['position'][1]]
                new_state[blank_x + move['position'][0]][blank_y + move['position'][1]] = 0
                next_states.append(new_state)
        return next_states

    # create the path of the solution
    def __create_path__(self, state):
        while state.get_parent():
            self.__path.append(state.get_state())
            state = state.get_parent()
        self.__path.append(state.get_state())
        self.__path.reverse()

    # print and save method
    def __save_result__(self, name, time):
        print('The puzzle is solved after ' + str(time))
        print('Solution path: ' + str(len(self.__path)) + ' steps.')
        print('Searched nodes: ' + str(self.__steps))
        with open(name + '.txt', 'w+') as file:
            file.write(name)
            file.write('\n\nInitial State:')
            for row in self.__init_state:
                file.write('\n' + str(row))
            file.write('\n\nGoal State:')
            for row in self.__goal_state:
                file.write('\n' + str(row))
            file.write('\n\nPuzzle solution path:')
            for state in self.__path:
                file.write('\n--------------------')
                for row in state:
                    file.write('\n' + str(row))
            file.write('\n--------------------')
            file.write('\n\nThe puzzle is solved after ' + str(time))
            file.write('\nShortest path: ' + str(len(self.__path)) + ' steps.')
            file.write('\nSearched nodes: ' + str(self.__steps) + '.')



