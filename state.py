import itertools


class State:

    def __init__(self, state, goal_state, depth, parent=None):
        self.__state = state
        self.__goal_state = goal_state
        self.__depth = depth
        self.__parent = parent
        self.__h1 = 0
        self.__h2 = 0

    # hamming distance
    def get_h1(self):
        current_state = list(itertools.chain.from_iterable(self.__state))
        goal_state = list(itertools.chain.from_iterable(self.__goal_state))
        for tile in current_state:
            if tile != 0 and tile != goal_state[current_state.index(tile)]:
                self.__h1 += 1
        return self.__h1

    # sum of permutation
    def get_h2(self):
        current_state = list(itertools.chain.from_iterable(self.__state))
        goal_state = list(itertools.chain.from_iterable(self.__goal_state))
        for tile in current_state:
            if tile != 0:
                for t in current_state[current_state.index(tile)+1:]:
                    if t != 0 and goal_state.index(t) < goal_state.index(tile):
                        self.__h2 += 1
        return self.__h2

    def get_parent(self):
        return self.__parent

    def get_state(self):
        return self.__state

    def get_depth(self):
        return self.__depth


if __name__ == '__main__':
    s = State([[5,0,8],[4,2,1],[7,3,6]],[[1,2,3],[4,5,6],[7,8,0]], 0)
    print(s.get_h1())
    print(s.get_h2())

