

class Coords:
    def __init__(self, loc):
        self.x = loc[0]
        self.y = loc[1]

    def __str__(self):
        return str([self.x, self.y])

    def subtract(self, second_coords):
        return Coords([second_coords.x - self.x, second_coords.y - self.y])

    def add(self, second_coords):
        return Coords([second_coords.x + self.x, second_coords.y + self.y])
