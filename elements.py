from __future__ import annotations
import numpy as np
import settings
import math

class Point:
    """
    Used to represent a Point of a tangram piece, note that the (0, 0) is at the top left and x goes positive downwards

    Attributes:
        x:  coordinate in the horizontal axis
        y:  coordinate in the vertical axis
    """

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x: float = x
        self.y: float = y

    def close_to(self, other: Point, distance=0.1) -> bool:
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
    """
    Vector class used for the direction of the edges
    """
    def __init__(self, x, y):
        super().__init__(x, y)

    def get_magnitude(self) -> float:
        """
        Gives the magnitude of the vector (its length)
        :return: the magnitude in px
        """
        return np.sqrt(self.x ** 2 + self.y ** 2)

    def get_normalized(self) -> Vector:
        """
        Gives the normalized vector
        :return: the normalized vector
        """
        magnitude = self.get_magnitude()
        return Vector(self.x / magnitude, self.y / magnitude)

    def get_angle_with(self, other) -> float:
        """
        Gives the angle_between_edges between this vector and another one
        :param other: other vector 
        :return: the angle_between_edges between the two vectors in degrees
        """
        dot_product = self.x * other.x + self.y * other.y
        magnitude = self.get_magnitude() * other.get_magnitude()
        res = math.degrees(math.acos(dot_product / magnitude))
        if self.x * other.y - self.y * other.x < 0:
            res = - res
        return res


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
        self.angle_between_edges = 0
        self.first_edge = None
        self.second_edge = None

    def compute_angle_between_edges(self):
        self.angle_between_edges = self.first_edge.direction.get_angle_with(self.second_edge.direction)

    def __repr__(self):
        return "Corner: " + str(self.x) + ", " + str(self.y)

    def __sub__(self, other):
        """
        Subtracts a point to the current one, i.e. subtracts its coordinate to it
        :param other: other point to subtract
        :return: the new point with the coordinates subtracted
        """
        new_corner = self
        new_corner.x = self.x - other.x
        new_corner.y = self.y - other.y
        return new_corner


class Piece:
    """
    Used to represent the tangram pieces

    Attributes:

        total_size:         side length of the square containing all the tangram pieces, determines the size of all the pieces
        side_length:        length of a side of the shape
        corners:             coordinates of the vertexes of the shape
        position_in_image:  coordinates of the shape in the image submitted by the user
        pivot_point:        coordinates of the pivot point the shapes refer to in order to rotate
        area:               area of the piece in pixels
        rotation:           angle_between_edges of rotation of the piece in degrees
        color:              color of the piece, RGB
        used:               True if the piece has been used on the shape
        name:               name of the piece
    """

    def __init__(self, color: (int, int, int) = (0, 0, 0)) -> None:
        self.total_size: int = settings.TANGRAM_SIDE_LENGTH  # width of the main square in pixels
        self.side_length: int = settings.TANGRAM_SIDE_LENGTH
        self.corners: list[Corner] = []
        self.position_in_image: Point = Point()
        self.pivot_point: Point = Point()
        self.area: int = 0
        self.rotation: int = 0
        self.color: tuple[int] = color
        self.used: bool = False
        self.name: str = ""
        self.max_corner_swap = 0
        self.number_of_corner_swap = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def next_corner(self) -> None:
        self.corners.append(self.corners.pop(0))
        for i in range(len(self.corners) - 1, -1, -1):
            self.corners[i] -= self.corners[0]
        self.pivot_point = self.corners[0]
        self.number_of_corner_swap += 1
        self.compute_edges()

    def rotate_shape_around_pivot(self, angle: float) -> None:
        """
        changes the coordinates of the shape to the new coordinates after a rotation of (angle_between_edges)°
        :param angle: angle_between_edges of rotation in degrees (clockwise)
        """
        angle = - angle  # to rotate counterclockwise
        self.rotation += angle
        angle = np.deg2rad(angle)
        for i in range(0, len(self.corners)):
            ox, oy = self.pivot_point.x, self.pivot_point.y
            px, py = self.corners[i].x, self.corners[i].y
            qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
            qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
            self.corners[i] = Corner(qx, qy)
        self.compute_edges()

    def get_points_in_image(self):
        """
        gives the coordinates of the shape in the image reference frame
        :return: the coordinates in a list of corners
        """
        coordinates_points = []
        for point in self.corners:
            coordinates_points.append(point + self.position_in_image)
        return coordinates_points

    def compute_edges(self):
        len_corners = len(self.corners)
        for i in range(0, len_corners):
            self.corners[i].first_edge = Edge(self.corners[i], self.corners[i - 1])
            self.corners[i].second_edge = Edge(self.corners[i], self.corners[(i + 1) % len_corners])
            self.corners[i].compute_angle_between_edges()

    def reset_rotation(self):
        self.rotate_shape_around_pivot(-self.rotation)


class Square(Piece):
    """
    Square tangram piece
    """

    def __init__(self, color=(0, 0, 0)):
        super().__init__(color)
        self.side_length = (np.sqrt(2) * self.total_size) / 4
        self.corners = [
            Corner(0, 0),
            Corner(self.side_length, 0),
            Corner(self.side_length, self.side_length),
            Corner(0, self.side_length)
        ]
        self.max_corner_swap = 4
        self.pivot_point = self.corners[0]
        self.compute_edges()
        self.area = self.side_length ** 2
        self.name = "Square"


class Triangle(Piece):
    """
    Triangle tangram piece
    """

    def __init__(self, color=(0, 0, 0)):
        super().__init__(color)
        self.side_length = 0
        self.max_corner_swap = 3

    def setup_triangle(self) -> None:
        """
        Sets up the triangle attributes
        """
        self.corners = [
            Corner(0, 0),
            Corner(self.side_length, 0),
            Corner(self.side_length, self.side_length),
        ]
        self.pivot_point = self.corners[0]
        self.compute_edges()
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
        self.corners = [
            Corner(0, 0),
            Corner(self.long_side_length, 0),
            Corner(3 * self.long_side_length / 2, self.height),
            Corner(self.long_side_length / 2, self.height)
        ]
        self.max_corner_swap = 4
        self.pivot_point = self.corners[0]
        self.compute_edges()
        self.area = self.long_side_length * self.height
        self.name = "Parallelogram"
        self.is_flipped = False

    def flip(self) -> None:
        """
        Flips the parallelogram (mirrored shape)
        """
        for corner in self.corners:
            corner.x *= -1
        self.is_flipped = not self.is_flipped
        self.compute_edges()
