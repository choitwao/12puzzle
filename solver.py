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

    def get_path(self):
        return self.__path

    def get_steps(self):
        return self.__steps

    def search_DFS(self, iteration=10000):
        print('\nStarting heuristic search using DFS......')
        tic = time.clock()
        open_list = []
        plain_open_list = []
        close_list = []
        init_state = State(self.__init_state, self.__goal_state, 0)
        open_list.append(init_state)
        # start searching
        while len(open_list) > 0 and self.__steps < iteration:
            self.__steps += 1
            current_state = open_list.pop()
            if current_state.get_state() in plain_open_list:
                plain_open_list.remove(current_state.get_state())
            # check if goal state is reached
            if current_state.get_state() == self.__goal_state:
                self.__create_path__(current_state)
                tic = time.clock() - tic
                break
            # search for children
            else:
                for state in self.__find_possible_states__(current_state.get_state()):
                    if state not in close_list and state not in plain_open_list:
                        new_state = State(state, self.__goal_state, current_state.get_depth() + 1, current_state)
                        open_list.append(new_state)
                        plain_open_list.append(state)
                close_list.append(current_state.get_state())
        if len(open_list) > 0 and self.__steps >= iteration:
            print('This puzzle is unsolvable.')
        else:
            self.__save_result__('puzzleDFS', tic)

    def search_BFS(self, heuristic_type=None, iteration=10000):
        print('\nStarting heuristic search using BFS......')
        tic = time.clock()
        open_list = Queue()
        plain_open_list = []
        close_list = []
        init_state = State(self.__init_state, self.__goal_state, 0)
        open_list.put(init_state)
        # start searching
        while open_list.qsize() and self.__steps < iteration:
            self.__steps += 1
            current_state = open_list.get()
            if current_state.get_state() in plain_open_list:
                plain_open_list.remove(current_state.get_state())
            # check if goal state is reached
            if current_state.get_state() == self.__goal_state:
                self.__create_path__(current_state)
                tic = time.clock() - tic
                break
            # search for children
            else:
                new_state_list = []
                for state in self.__find_possible_states__(current_state.get_state()):
                    if state not in close_list and state not in plain_open_list:
                        new_state = State(state, self.__goal_state, current_state.get_depth() + 1, current_state)
                        new_state_list.append(new_state)
                        plain_open_list.append(state)
                if heuristic_type == 'h1':
                    new_state_list = sorted(new_state_list, key=lambda x: x.get_h1())
                else:
                    new_state_list = sorted(new_state_list, key=lambda x: x.get_h2())
                for state in new_state_list:
                    open_list.put(state)
                close_list.append(current_state.get_state())
        if open_list.qsize() and self.__steps >= iteration:
            print('This puzzle is unsolvable.')
        else:
            self.__save_result__('puzzleBFS-h1' if heuristic_type is 'h1' else 'puzzleBFS-h2', tic)

    def search_Astar(self, heuristic_type=None, iteration=10000):
        print('\nStarting heuristic search using A*......')
        tic = time.clock()
        open_list = PriorityQueue()
        plain_open_list = []
        close_list = []
        init_state = State(self.__init_state, self.__goal_state, 0)
        open_list.put(init_state)
        # start searching
        while open_list.qsize() and self.__steps < iteration:
            self.__steps += 1
            current_state = open_list.get()
            if current_state.get_state() in plain_open_list:
                plain_open_list.remove(current_state.get_state())
            # check if goal state is reached
            if current_state.get_state() == self.__goal_state:
                self.__create_path__(current_state)
                tic = time.clock() - tic
                break
            # search for children
            else:
                for state in self.__find_possible_states__(current_state.get_state()):
                    if state not in close_list and state not in plain_open_list:
                        new_state = State(state, self.__goal_state, current_state.get_depth() + 1, current_state)
                        plain_open_list.append(state)
                        if heuristic_type == 'h1':
                            new_state.get_h1()
                            open_list.put(new_state)
                        else:
                            new_state.get_h2()
                            open_list.put(new_state)
                close_list.append(current_state.get_state())
        if open_list.qsize() and self.__steps >= iteration:
            print('This puzzle is unsolvable.')
        else:
            self.__save_result__('puzzleAs-h1' if heuristic_type is 'h1' else 'puzzleAs-h2', tic)

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
        # down, up, right, left, down_left, down_right, up_left, up_right object
        move_position = {
            'down': {
                'exist': blank_x > 0,
                'position': [-1, 0]
            },
            'up': {
                'exist': blank_x < len(state) - 1,
                'position': [1, 0]
            },
            'right': {
                'exist': blank_y > 0,
                'position': [0, -1]
            },
            'left': {
                'exist': blank_y < len(state[0]) - 1,
                'position': [0, 1]
            },
            'down_right': {
                'exist': blank_x > 0 and blank_y > 0,
                'position': [-1, -1]
            },
            'down_left': {
                'exist': blank_x > 0 and blank_y < len(state[0]) - 1,
                'position': [-1, 1]
            },
            'up_right': {
                'exist': blank_x < len(state) - 1 and blank_y > 0,
                'position': [1, -1]
            },
            'up_left': {
                'exist': blank_x < len(state) - 1 and blank_y < len(state[0]) - 1,
                'position': [1, 1]
            }
        }
        for key, move in move_position.items():
            if move['exist']:
                new_state = copy.deepcopy(state)
                new_state[blank_x][blank_y] = state[blank_x + move['position'][0]][blank_y + move['position'][1]]
                new_state[blank_x + move['position'][0]][blank_y + move['position'][1]] = 0
                next_states.append(new_state)
        return next_states

    def __create_path__(self, state):
        while state.get_parent():
            self.__path.append(state.get_state())
            state = state.get_parent()
        self.__path.append(state.get_state())
        self.__path.reverse()

    def __save_result__(self, name, time):
        print('The puzzle is solved after ' + str(time))
        print('Shortest path: ' + str(len(self.__path)) + ' steps.')
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



