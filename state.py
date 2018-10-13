import random
import sys
import os
import time
from copy import deepcopy


class State:

    def __init__(self, state, goal_state, depth, parent=None):
        self.__state = state
        self.__goal_state = goal_state
        self.__depth = depth
        self.__parent = parent
        self.__h1 = None
        self.__h2 = None

    def __calculate_h1(self):
        pass

    def __calculate_h2(self):
        pass

    def get_h1(self):
        return self.__h1

    def get_h2(self):
        return self.__h2

    def get_parent(self):
        return self.__parent

    def get_state(self):
        return self.__state

    def get_depth(self):
        return self.__depth

