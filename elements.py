import numpy as np


class Shape:
    def __init__(self):
        self.total_size = 360  # width of the main square in pixels
        self.points = []
        self.reference_points = Point()

    def rotate_shape_around_pivot(self, angle):
        angle = np.deg2rad(angle)
        for i in range(0, len(self.points)):
            ox, oy = self.reference_points.x, self.reference_points.y
            px, py = self.points[i].x, self.points[i].y
            qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
            qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
            self.points[i] = Point(int(qx), int(qy))

class Point:
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"x:{self.x}, y:{self.y}"

    def __add__(self, other):
        new_pt = Point(0,0)
        new_pt.x = self.x + other.x
        new_pt.y = self.y + other.y
        return new_pt

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

class Triangle(Shape):
    def __init__(self):
        super().__init__()
        self.side_length = 0
        self.reference_points = Point(0,0)
        self.setup_triangle()

    def setup_triangle(self):
        self.points = [
            Point(0,0),
            Point(0,self.side_length),
            Point(self.side_length,0)
        ]

class SmallTriangle(Triangle):
    def __init__(self):
        super(SmallTriangle, self).__init__()
        self.side_length = (self.total_size * np.sqrt(2)) / 4
        self.setup_triangle()

class MediumTriangle(Triangle):
    def __init__(self):
        super(MediumTriangle, self).__init__()
        self.side_length = self.total_size / 2
        self.setup_triangle()

class LargeTriangle(Triangle):
    def __init__(self):
        super(LargeTriangle, self).__init__()
        self.side_length = self.total_size
        self.setup_triangle()


class Parallelogram(Shape):
    def __init__(self):
        super().__init__()
        self.points = [

        ]
        self.reference_point = Point(0,0)

if __name__ == '__main__':
    #J'ai pas mis le parallelogramme pour l'instant pour vérifier que les autres pièces marchentg
    pieces_tangram = [
        Square(),
        SmallTriangle(),
        SmallTriangle(),
        MediumTriangle(),
        LargeTriangle(),
        LargeTriangle()
    ]
    #Montre les positions des points avant
    triangle_1 = pieces_tangram[1]
    for point in triangle_1.points:
        print(point)

    triangle_1.rotate_shape_around_pivot(180)
    #Montre les positions après rotation de 90deg
    # J'ai arrondi les valeurs parce que sinon on avait des décalages au bout de n rotations
    for point in triangle_1.points:
        print(point)
