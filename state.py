import itertools


class State:

    def __init__(self, state, goal_state, depth, parent=None):
        self.__state = state
        self.__goal_state = goal_state
        self.__depth = depth
        self.__parent = parent
        self.__heuristic = 0

    # hamming distance
    def get_h1(self):
        current_state = list(itertools.chain.from_iterable(self.__state))
        goal_state = list(itertools.chain.from_iterable(self.__goal_state))
        for tile in current_state:
            if tile != 0 and tile != goal_state[current_state.index(tile)]:
                self.__heuristic += 1
        self.__heuristic += self.__depth
        return self.__heuristic

    # sum of permutation
    def get_h2(self):
        current_state = list(itertools.chain.from_iterable(self.__state))
        goal_state = list(itertools.chain.from_iterable(self.__goal_state))
        for tile in current_state:
            if tile != 0:
                for t in current_state[current_state.index(tile)+1:]:
                    if t != 0 and goal_state.index(t) < goal_state.index(tile):
                        self.__heuristic += 1
        self.__heuristic += self.__depth
        return self.__heuristic

    def get_parent(self):
        return self.__parent

    def get_state(self):
        return self.__state

    def get_depth(self):
        return self.__depth

    def __lt__(self, other):
        return self.__heuristic < other.__heuristic

    def __eq__(self, other):
        return self.__heuristic == other.__heuristic

    def __gt__(self, other):
        return self.__heuristic > other.__heuristic
