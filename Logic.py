from State import State
import os
from queue import PriorityQueue


class Logic:
    def __init__(self, state: State):
        self.state: State = state
        self.moveNumber = 0
        self.path=[]
        pass

    def UniformCostSearch(self):
        priority_queue = []
        dist = {}
        dist[self.state.hashCode()] = 0
        priority_queue.append((0, self.state))
        self.moveNumber=0

        while priority_queue:
            minState = priority_queue.pop(0)
            weight = minState[0]
            self.state: State = minState[1]
            self.moveNumber += 1

            if self.state.is_goal():
                cost = self.state.getCost()
                self.pathTrace()
                print(f'done with {self.moveNumber} visited states')
                print(f'Path cost is: {cost}')
                return True

            if weight > dist.get(self.state.hashCode(), 100000):
                print('here')
                continue

            nextState: State
            for nextState in self.state.nextState():
                if dist.get(nextState.hashCode(), 100000) > nextState.getCost():
                    dist[nextState.hashCode()] = nextState.getCost()
                    priority_queue.append((nextState.getCost(), nextState))
                    priority_queue.sort(reverse=False, key=lambda x: x[0])
                    pass

        pass

    def aStareOrdinary(self, heuristicNumber):
        self.state.setHeuristicNumber(heuristicNumber)
        priority_queue = PriorityQueue()
        dist = {}
        dist[self.state.hashCode()] = 0
        priority_queue.put(self.state)
        self.moveNumber=0

        while not priority_queue.empty():
            self.state: State = priority_queue.get()
            self.moveNumber += 1

            if self.state.is_goal():
                cost = self.state.getCost()
                self.pathTrace()
                print(f'done with {self.moveNumber} visited states')
                print(f'Path cost is: {cost}')
                return True

            if self.state.f() > dist.get(self.state.hashCode(), 100000):
                continue

            nextState: State
            for nextState in self.state.nextState():
                if dist.get(nextState.hashCode(), 100000) > nextState.f():
                    dist[nextState.hashCode()] = nextState.f()
                    priority_queue.put(nextState)
                    pass
        pass

    def pathTrace(self):
        i = 0
        self.path.clear()
        
        while(self.state.parent):
            self.path.append(self.state)
            self.state.printState()
            print('_______________________________')
            self.state = self.state.parent
            i += 1
        self.state.printState()
        print(f'path long is: {i}')
