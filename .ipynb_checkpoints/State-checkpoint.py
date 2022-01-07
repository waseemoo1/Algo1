import copy
import numpy as np


class State:
    def __init__(self):
        self.cells = {}
        self.cells['I'] = self.stateStaticInitialization()
        self.p = 0
        pass

    def move(self):
        pass

    def nextState(self):
        pass

    def is_goal(self):
        pass

    def stateStaticInitialization(self):
        test_data_file = open("input.txt", 'r')
        test_data_list = test_data_file.readlines()
        test_data_file.close()

        return np.array([1, 2, 3, 4])

    def printState(self):
        pass

    def getEmptyCells(self):
        pass

    def getValidMoves(self, emptyCells):
        pass

    def isLegal(self, position):
        pass

    def getCar(self, position):
        pass

    def canMove(self, unit, _from, to):
        pass

    def setHeuristic(self):
        pass

    def f(self):
        pass

    def hashCode(self) -> str:
        hashString: str = ''
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j]:
                    hashString += str(self.cells[i][j].number)
                else:
                    hashString += 'n'

        return hashString

    def __gt__(self, other):
        if self.f() > other.f():
            return True
        elif self.f() == other.f():
            if self.heuristic > other.heuristic:
                return True
            else:
                return False
        return False

    def __lt__(self, other):
        if self.f() < other.f():
            return True
        elif self.f() == other.f():
            if self.heuristic < other.heuristic:
                return True
            else:
                return False
        return False

    def __eq__(self, __o: object) -> bool:
        return self.f() == __o.f() and self.heuristic == __o.heuristic
