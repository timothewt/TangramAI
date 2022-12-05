from math import floor

import numpy as np
import settings

class Point:
    """
    Used to represent a Point of a tangram piece, note that the (0, 0) is at the top left and x goes positive downwards

    Attributes:
        x:  coordinate in the horizontal axis
        y:  coordinate in the vertical axis
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x: int = int(x)
        self.y: int = int(y)

    def close_to(self, other, distance=0.1) -> bool:
        """
        Checks if the current point is close to another point
        :param other: the other point
        :param distance: the distance to check
        :return: True if the current point is close to the other one, False otherwise
        """
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2) < distance

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        """
        displays the coordinates in a string
        :return: the string "x:(x coordinate), y:(y coordinate)"
        """
        return f"x:{self.x}, y:{self.y}"

    def __sub__(self, other):
        """
        Subtracts a point to the current one, i.e. subtracts its coordinate to it
        :param other: other point to subtract
        :return: the new point with the coordinates subtracted
        """
        new_pt = Point(0, 0)
        new_pt.x = self.x - other.x
        new_pt.y = self.y - other.y
        return new_pt

    def __mul__(self, other):
        """
        Multiplies a point to the current one, i.e. multiplies its coordinate to it
        :param other: other point to multiply
        :return: the new point with the coordinates multiplied
        """
        new_pt = Point(0, 0)
        new_pt.x = self.x * other.x
        new_pt.y = self.y * other.y
        return new_pt

    def __truediv__(self, other):
        """
        Divides a point to the current one, i.e. divides its coordinate to it
        :param other: other point to divide
        :return: the new point with the coordinates divided
        """
        new_pt = Point(0, 0)
        new_pt.x = self.x / other.x
        new_pt.y = self.y / other.y
        return new_pt

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other):
        """
        Adds a point to the current one, i.e. adds its coordinate to it
        :param other: other point to add
        :return: the new point with the coordinates added
        """
        new_pt = Point(0, 0)
        new_pt.x = self.x + other.x
        new_pt.y = self.y + other.y
        return new_pt


class Vector(Point):
    def __init__(self, x, y):
        super().__init__(x, y)


    def get_magnitude(self):
        return np.sqrt(self.x ** 2 + self.y ** 2)

    def get_normalized(self):
        magnitude = self.get_magnitude()
        return Vector(self.x / magnitude, self.y / magnitude)

    def get_angle_between(self, other):
        dot_product = self.x * other.x + self.y * other.y
        magnitude = self.get_magnitude() * other.get_magnitude()
        return np.degrees(np.acos(dot_product / magnitude))



class Edge:
    def __init__(self, start_point: Point, end_point : Point):
        self.start_point = start_point
        self.end_point = end_point
        self.direction = Vector(end_point.x - start_point.x, end_point.y - start_point.y)

    def __str__(self):
        return f"Edge from {self.start_point} with direction {self.direction}"

class Corner(Point):
    def __init__(self, x, y, edges_from_corner : list = None):
        super().__init__(x, y)
        self.edges_from_corner = edges_from_corner


class Piece:
    """
    Used to represent the tangram pieces

    Attributes:

        total_size:         side length of the square containing all the tangram pieces, determines the size of all the pieces
        side_length:        length of a side of the shape
        points:             coordinates of the vertexes of the shape
        position_in_image:  coordinates of the shape in the image submitted by the user
        pivot_point:        coordinates of the pivot point the shapes refer to in order to rotate
        area:               area of the piece in pixels
        rotation:           angle of rotation of the piece in degrees
        color:              color of the piece, RGB
        used:               True if the piece has been used on the shape
        corners_visited:    list of the corners on which the piece has already been placed
        name:               name of the piece
    """

    def __init__(self, color: (int, int, int) = (0, 0, 0)) -> None:
        self.total_size: int = settings.TANGRAM_SIDE_LENGTH  # width of the main square in pixels
        self.side_length: int = settings.TANGRAM_SIDE_LENGTH
        self.points: list[Point] = []
        self.position_in_image: Point = Point()
        self.pivot_point: Point = Point()
        self.area: int = 0
        self.rotation: int = 0
        self.color: tuple[int] = color
        self.used: bool = False
        self.corners_visited: list[Point] = []
        self.name: str = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def rotate_shape_around_pivot(self, angle: float) -> None:
        """
        changes the coordinates of the shape to the new coordinates after a rotation of (angle)°
        :param angle: angle of rotation in degrees (clockwise)
        """
        self.rotation += angle
        self.rotation %= 360
        angle = np.deg2rad(angle)
        for i in range(0, len(self.points)):
            ox, oy = self.pivot_point.x, self.pivot_point.y
            px, py = self.points[i].x, self.points[i].y
            qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
            qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
            self.points[i] = Point(qx, qy)

    def get_points_in_image(self):
        """
        gives the coordinates of the shape in the image reference frame
        :return: the coordinates in a list of points
        """
        coordinates_points = []
        for point in self.points:
            coordinates_points.append(point + self.position_in_image)
        return coordinates_points


class Square(Piece):
    """
    Square tangram piece
    """

    def __init__(self, color=(0, 0, 0)):
        super().__init__(color)
        self.side_length = (np.sqrt(2) * self.total_size) / 4
        self.points = [
            Point(0, 0),
            Point(self.side_length, 0),
            Point(self.side_length, self.side_length),
            Point(0, self.side_length)
        ]
        self.pivot_point = self.points[0]
        self.area = self.side_length ** 2
        self.name = "Square"


class Triangle(Piece):
    """
    Triangle tangram piece
    """

    def __init__(self, color=(0, 0, 0)):
        super().__init__(color)
        self.side_length = 0

    def setup_triangle(self) -> None:
        """
        Sets up the triangle attributes
        """
        self.points = [
            Point(0, 0),
            Point(self.side_length, 0),
            Point(self.side_length, self.side_length),
        ]
        self.pivot_point = self.points[0]
        self.area = (self.side_length ** 2) // 2


class SmallTriangle(Triangle):
    """
    Small triangle tangram piece
    """

    def __init__(self, color=(0, 0, 0)):
        super().__init__(color)
        self.side_length = (self.total_size * np.sqrt(2)) / 4
        self.setup_triangle()
        self.name = "Small Triangle"


class MediumTriangle(Triangle):
    """
    Medium triangle tangram piece
    """

    def __init__(self, color=(0, 0, 0)):
        super().__init__(color)
        self.side_length = self.total_size / 2
        self.setup_triangle()
        self.name = "Medium Triangle"


class LargeTriangle(Triangle):
    """
    Large triangle tangram piece
    """

    def __init__(self, color=(0, 0, 0)):
        super().__init__(color)
        self.side_length = (self.total_size * np.sqrt(2)) / 2
        self.setup_triangle()
        self.name = "Large Triangle"


class Parallelogram(Piece):
    """
    Parallelogram tangram piece
    """

    def __init__(self, color=(0, 0, 0)):
        super().__init__(color)
        self.long_side_length = self.total_size / 2
        self.height = self.total_size / 4
        self.points = [
            Point(0, 0),
            Point(self.long_side_length, 0),
            Point(3 * self.long_side_length / 2, self.height),
            Point(self.long_side_length / 2, self.height)
        ]
        self.pivot_point = self.points[0]
        self.area = self.long_side_length * self.height
        self.name = "Parallelogram"
        self.is_flipped = False

    def flip(self) -> None:
        """
        Flips the parallelogram (mirrored shape)
        """
        for point in self.points:
            point.x *= -1
        self.is_flipped = True
