import numpy as np


class Point:
    """
    Used to represent a Point of a tangram piece, note that the (0, 0) is at the top left and x goes positive downwards
    ----
    x: int
        coordinate in the horizontal axis
    y: int
        coordinate in the vertical axis
    """
    def __init__(self, x:float = 0.0, y: float = 0.0) -> None:
        self.x = round(x)
        self.y = round(y)

    def __str__(self) -> str:
        """
        displays the coordinates in a string
        :return: the string "x:(x coordinate), y:(y coordinate)"
        """
        return f"x:{self.x}, y:{self.y}"

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


class Shape:
    """
    Used to represent the tangram pieces
    ---
    total_size: int
        side length of the square containing all the tangram pieces, determines the size of all the pieces
    side_length: int
        length of a side of the shape
    points: Point[]
        coordinates of the vertexes of the shape
    position_in_image: Point
        coordinates of the shape in the image submitted by the user
    pivot_point: Point
        coordinates of the pivot point the shapes refer to in order to rotate
    color: int
        color of the piece, just a level of gray for the moment
    """
    def __init__(self, color: int = 0) -> None:
        self.total_size = 280  # width of the main square in pixels
        self.side_length = 280
        self.points = []
        self.position_in_image = Point()
        self.pivot_point = Point()
        self.color = color
        self.used = False

    def rotate_shape_around_pivot(self, angle: float) -> None:
        """
        changes the coordinates of the shape to the new coordinates after a rotation of (angle)°
        :param angle: angle of rotation in degrees (clockwise)
        """
        angle = np.deg2rad(angle)
        for i in range(0, len(self.points)):
            ox, oy = self.pivot_point.x, self.pivot_point.y
            px, py = self.points[i].x, self.points[i].y
            qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
            qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
            self.points[i] = Point(qx, qy)

    def get_points_in_image(self) -> list[Point]:
        """
        gives the coordinates of the shape in the image reference frame
        :return: the coordinates in a list of points
        """
        coordinates_points = []
        for point in self.points:
            coordinates_points.append(point + self.position_in_image)
        return coordinates_points


class Square(Shape):
    """
    Square tangram piece
    """
    def __init__(self, color):
        super().__init__(color)
        self.side_length = (np.sqrt(2) * self.total_size) / 4
        self.points = [
            Point(0, 0),
            Point(self.side_length, 0),
            Point(self.side_length, self.side_length),
            Point(0, self.side_length)
        ]
        self.pivot_point = self.points[0]


class Triangle(Shape):
    """
    Triangle tangram piece
    """
    def __init__(self, color):
        super().__init__(color)
        self.side_length = 0
        self.setup_triangle()

    def setup_triangle(self) -> None:
        """
        Sets up the triangle attributes
        """
        self.points = [
            Point(0, 0),
            Point(0, self.side_length),
            Point(self.side_length, 0)
        ]
        self.pivot_point = self.points[0]


class SmallTriangle(Triangle):
    """
    Small triangle tangram piece
    """
    def __init__(self, color):
        super(SmallTriangle, self).__init__(color)
        self.side_length = (self.total_size * np.sqrt(2)) / 4
        self.setup_triangle()


class MediumTriangle(Triangle):
    """
    Medium triangle tangram piece
    """
    def __init__(self, color):
        super(MediumTriangle, self).__init__(color)
        self.side_length = self.total_size / 2
        self.setup_triangle()


class LargeTriangle(Triangle):
    """
    Large triangle tangram piece
    """
    def __init__(self, color):
        super(LargeTriangle, self).__init__(color)
        self.side_length = (self.total_size * np.sqrt(2)) / 2
        self.setup_triangle()


class Parallelogram(Shape):
    """
    Parallelogram tangram piece
    """
    def __init__(self, color):
        super().__init__(color)
        self.long_side_length = self.total_size / 2
        self.height = self.total_size / 4
        """ height = |
           ________
          /   |   /
         /    |  /
        /_____|_/
        """
        self.points = [
            Point(self.long_side_length / 2, 0),
            Point(3 * self.long_side_length / 2, 0),
            Point(self.long_side_length, self.height),
            Point(0, self.height)
        ]
        self.pivot_point = self.points[0]

