from collections import deque

from utils.helpers import distance


class Tracker:
    def __init__(self, maxlen=None):
        self.positions = deque(maxlen=maxlen)


    def update(self, position):
        if position is None:
            return

        self.positions.append(position)


    def velocity(self):
        if len(self.positions) < 2:
            return 0

        total = 0

        for i in range(1, len(self.positions)):
            total += distance(self.positions[i - 1], self.positions[i])

        return total / (len(self.positions) - 1)


    def trajectory(self):
        return list(self.positions)
