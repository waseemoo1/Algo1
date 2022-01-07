import copy
import numpy as np


class State:
    def __init__(self):
        self.cells = initialization()
        self.loadPlaces, self.dropPlaces = self.initilaizPlaces()
        self.start_place = self.getTruckPosition()
        self.cost = 0
        self.heuristic = 0
        self.truckLoads = []
        self.parent = None
        self.HeuristicNumber = 1
        pass

    def move(self, newPosition, oldPosition):
        self.cells[newPosition[0], newPosition[1]] = 'T'

        # not get the load
        load_num = self.loadPlaces.get((oldPosition[0], oldPosition[1]), -1)
        if load_num != -1:
            self.cells[oldPosition[0], oldPosition[1]] = f'P{load_num}'
            return

        # not give the load to the drop place
        drop_num = self.dropPlaces.get((oldPosition[0], oldPosition[1]), -1)
        if drop_num != -1:
            self.cells[oldPosition[0], oldPosition[1]] = f'D{drop_num}'
            return

        self.cells[oldPosition[0], oldPosition[1]] = '.'
        pass

    def nextState(self):
        states = []

        truck = self.getTruckPosition()
        truckPosition = (truck[0], truck[1])

        moves = self.getValidMoves(truck)

        # truck in load place
        if self.loadPlaces.get(truckPosition, -1) != -1:

            load_num = self.loadPlaces.get(truckPosition)

            new_state = copy.deepcopy(self)
            new_state.parent = self
            new_state.truckLoads = np.append(new_state.truckLoads, load_num)
            new_state.loadPlaces.pop(truckPosition)
            states.append(new_state)
            # todo should add weight
            pass

        # truck in drop place
        if self.dropPlaces.get(truckPosition, -1) != -1:
            drop_num = self.dropPlaces.get(truckPosition)

            # truck have the drop
            if drop_num in self.truckLoads:

                new_state = copy.deepcopy(self)
                new_state.parent = self
                new_state.truckLoads = new_state.truckLoads[new_state.truckLoads != drop_num]
                new_state.dropPlaces.pop(truckPosition)
                states.append(new_state)
                # todo should add weight

        for x in moves:
            new_state = copy.deepcopy(self)
            new_state.parent = self
            new_state.cost += self.getLoadsCost() + 1
            new_state.setHeuristic()
            new_state.move(x[1], truck)
            states.append(new_state)

        return states

    def is_goal(self):
        return len(self.dropPlaces) == 0 and np.all(self.getTruckPosition() == self.start_place)

    def getCost(self):
        return self.cost

    def getTruckPosition(self):
        return np.array(np.where(self.cells == 'T')).flatten()

    def printState(self):
        print()
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                print("{0:^8}".format(self.cells[i][j]), end=' ')

            print()

    def getValidMoves(self, truck):
        cell = truck
        moves = []

        up = (cell[0] - 1, cell[1])

        if self.isLegal(up):
            moves.append(('Up', up))

        down = (cell[0] + 1, cell[1])

        if self.isLegal(down):
            moves.append(('Down', down))

        right = (cell[0], cell[1] + 1)
        if self.isLegal(right):
            moves.append(("Right", right))

        left = (cell[0], cell[1] - 1)
        if self.isLegal(left):
            moves.append(("Left", left))

        return moves

    def isLegal(self, position):
        return (0 <= position[0] < self.cells.shape[0]) and (0 <= position[1] < self.cells.shape[1]) and (self.cells[position[0], position[1]] != '#')

    def getLoadsCost(self):
        return len(self.truckLoads)

    def setHeuristicNumber(self, HeuristicNumber):
        self.HeuristicNumber = HeuristicNumber

    def manhattenDistance(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

    def heuristic_1(self):
        truckPosition = self.getTruckPosition()
        return self.manhattenDistance(truckPosition, self.start_place)

    def heuristic_2(self):
        h = 0

        truckPosition = self.getTruckPosition()
        for i in self.loadPlaces.items():
            h += (self.manhattenDistance(i[0],
                  truckPosition) * len(self.truckLoads))
            for j in self.dropPlaces.items():
                if(j[1] == i[1]):
                    h += (self.manhattenDistance(i[0],
                          j[0]) * len(self.truckLoads))

        for i in self.truckLoads:
            for j in self.dropPlaces.items():
                if(j[1] == i):
                    h += (self.manhattenDistance(truckPosition,
                          j[0]) * len(self.truckLoads))

        return h

    def heuristic_3(self):
        h = 0

        truckPosition = self.getTruckPosition()

        for i in self.loadPlaces.items():
            temp = 0
            temp += (self.manhattenDistance(i[0],
                     truckPosition) * len(self.truckLoads))
            for j in self.dropPlaces.items():
                if(j[1] == i[1]):
                    temp += (self.manhattenDistance(i[0],
                             j[0]) * len(self.truckLoads))
            h = max(temp, h)

        return h
    

    def setHeuristic(self):

        if self.HeuristicNumber == 1:
            self.heuristic = self.heuristic_1()
            return

        if self.HeuristicNumber == 2:
            self.heuristic = self.heuristic_2()
            return

        if self.HeuristicNumber == 3:
            self.heuristic = self.heuristic_3()
            return

        pass

    def f(self):
        return self.cost + self.heuristic

    def hashCode(self) -> str:
        hashString: str = ''
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                hashString += str(self.cells[i][j])

        for i in self.truckLoads:
            hashString += str(i)

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

    def initilaizPlaces(self):
        loadPlaces = {}
        dropPlaces = {}
        for i in range(999):
            Pposition = np.array(np.where(self.cells == f'P{i}')).flatten()
            Dposition = np.array(np.where(self.cells == f'D{i}')).flatten()
            if len(Pposition) == 0:
                break
            loadPlaces[(Pposition[0], Pposition[1])] = i
            dropPlaces[(Dposition[0], Dposition[1])] = i
        return loadPlaces, dropPlaces


def initialization():
    input_file = open("input.txt", 'r')
    input_data_list = input_file.read().splitlines()
    input_file.close()

    celles = []
    for record in input_data_list:
        all_values = record.split(' ')
        celles.append(all_values)

    celles = np.asarray(celles)

    return celles
