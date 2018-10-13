from queue import PriorityQueue, Queue
from state import State
import time


class Solver:

    def __init__(self, init_state, goal_state, width):
        self.__init_state = self.__convert_state__(init_state, width)
        self.__goal_state = self.__convert_state__(goal_state, width)
        self.__path = []
        self.__steps = 0

    def get_path(self):
        return self.__path

    def __convert_state__(self, state, width):
        converted_state = [state[tile:tile+width] for tile in range(0, len(state), width)]
        return converted_state

    def search_BFS(self):
        tic = time.clock()
        iteration = 2000
        depth = 0
        open_list = Queue()
        close_list = []
        init_state = State(self.__init_state, self.__goal_state, depth)
        open_list.put(init_state)
        # start searching
        while open_list.qsize() and iteration > 0:
            iteration -= 1
            current_state = open_list.get()
            # skip closed state
            if str(current_state.get_state()) in close_list:
                continue
            # check if goal state is reached
            elif str(current_state.get_state()) == str(self.__init_state):
                while current_state.get_parent():
                    self.__path.append(current_state)
                    current_state = current_state.get_parent()
                    tic = time.clock() - tic
                break
            # search for children
            else:
                pass


if __name__ == '__main__':
    s = Solver([2, 3, 5, 2, 1, 5, 6, 2, 1, 42, 21, 66], [2, 3, 5, 2, 1, 5, 6, 2, 1, 42, 21, 66], 4)

