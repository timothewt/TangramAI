import numpy as np


class Shape:
    def __init__(self):
        self.total_size = 360  # width of the main square in pixels


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Square(Shape):
    def __init__(self):
        super().__init__()
        self.width = (np.sqrt(2) * self.total_size) / 4
        self.points = [
            Point(0, 0),
            Point(self.width, 0),
            Point(0, self.width),
            Point(self.width, self.width)
        ]
        self.reference_point = Point(0, 0)


if __name__ == '__main__':
    sq = Square()
