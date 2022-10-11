import numpy as np


class Shape:
    def __init__(self):
        self.total_size = 280  # width of the main square in pixels
        self.points = []
        self.position_in_image = Point()
        self.pivot_point = Point()
        self.color = (0,0,0)

    def rotate_shape_around_pivot(self, angle):
        angle = np.deg2rad(angle)
        for i in range(0, len(self.points)):
            ox, oy = self.pivot_point.x, self.pivot_point.y
            px, py = self.points[i].x, self.points[i].y
            qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
            qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
            self.points[i] = Point(qx, qy)

    def get_points_in_image(self):
        coordinates_points = []
        for point in self.points:
            coordinates_points.append(point + self.position_in_image)
        return coordinates_points


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = round(x)
        self.y = round(y)

    def __str__(self):
        return f"x:{self.x}, y:{self.y}"

    def __add__(self, other):
        new_pt = Point(0, 0)
        new_pt.x = self.x + other.x
        new_pt.y = self.y + other.y
        return new_pt


class Square(Shape):
    def __init__(self):
        super().__init__()
        self.side_length = (np.sqrt(2) * self.total_size) / 4
        self.pivot_point = Point(self.side_length / 2, self.side_length / 2)
        self.points = [
            Point(0, 0),
            Point(self.side_length, 0),
            Point(0, self.side_length),
            Point(self.side_length, self.side_length)
        ]
    def _calculate_area(self, A, B, C):
        area = abs((B.x * A.y - A.x * B.y) + (C.x * B.y - B.x * C.y) + (A.x * C.y - C.x * A.y)) / 2
        return area

    def contains_point(self, M):
        A,B,C,D = self.get_points_in_image()
        sum_area = self._calculate_area(A,M,D) + self._calculate_area(D,M,C)
        sum_area += self._calculate_area(C,M,B) + self._calculate_area(M,B,A)

        area_square = self.side_length*self.side_length
        return sum_area < area_square

class Triangle(Shape):
    def __init__(self):
        super().__init__()
        self.side_length = 0
        self.setup_triangle()

    def setup_triangle(self):
        self.pivot_point = Point(self.side_length / 3, self.side_length / 3)
        self.points = [
            Point(0, 0),
            Point(0, self.side_length),
            Point(self.side_length, 0)
        ]

    def contains_point(self, M):  # M being the point we want to know if it's in the triangle
        A, B, C = self.get_points_in_image()
        s = ((M.x - A.x) * (B.y - A.y) - (M.y - A.y) * (B.x - A.x)) / (
                    (C.x - A.x) * (B.y - A.y) - (C.y - A.y) * (B.x - A.x))
        t = ((M.y - A.y) * (C.x - A.x) - (M.x - A.x) * (C.y - A.y)) / (
                    (B.y - A.y) * (C.x - A.x) - (B.x - A.x) * (C.y - A.y))
        return 0 <= s <= 1 and 0 <= t <= 1 and s + t <= 1


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
        self.side_length = (self.total_size * np.sqrt(2)) / 2
        self.setup_triangle()


class Parallelogram(Shape):
    def __init__(self):
        super().__init__()
        self.long_side_length = self.total_size / 2
        self.height = self.total_size / 4
        """ height = |
           ________
          /   |   /
         /    |  /
        /_____|_/
        """
        self.pivot_point = Point(3 * self.long_side_length / 4, self.height / 2)
        self.points = [
            Point(self.long_side_length / 2, 0),
            Point(3 * self.long_side_length / 2, 0),
            Point(self.long_side_length, self.height),
            Point(0, self.height)
        ]


if __name__ == '__main__':
    # J'ai pas mis le parallelogramme pour l'instant pour vérifier que les autres pièces marchent
    pieces_tangram = [
        Square(),
        SmallTriangle(),
        SmallTriangle(),
        MediumTriangle(),
        LargeTriangle(),
        LargeTriangle(),
        Parallelogram()
    ]
    # Montre les positions des points avant
    triangle_1 = pieces_tangram[6]
    for point in triangle_1.points:
        print(point)

    triangle_1.rotate_shape_around_pivot(180)
    # Montre les positions après rotation de 90deg
    # J'ai arrondi les valeurs parce que sinon on avait des décalages au bout de n rotations
    for point in triangle_1.points:
        print(point)
