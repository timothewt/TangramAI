from __future__ import annotations
import cv2 as cv
from elements import *
from settings import MIN_SUB_PUZZLE_AREA

### CALCULATIONS UTILS ###

def approx_eq(a: float, b: float) -> bool:
    """
    Used to compare angles that are the same, but can differ from a few degrees due to bad precision
    :param a: first value to compare
    :param b: second value to compare
    :return: True if the angle are approximately equal, False otherwise
    """
    return b - 2 < a < b + 2

def get_duplicate(values: list[float]) -> float:
    """
    Gives the approximate duplicated values in a list. Used to approximate the equality between angles
    :param values: list of values in there are duplicates
    :return: the duplicate value
    """
    result = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if approx_eq(abs(values[i]), 180) and approx_eq(-values[i], values[j]):  # we may have to similar angles like 180 and -180
                result = values[i]
            if approx_eq(values[i], values[j]):
                result = values[i]
    return result

def accept_new_piece(prev_img: np.ndarray([], dtype=int), candidate_img: np.ndarray([], dtype=int),
                     piece_area: int) -> bool:
    """
    Says if the placement of the new piece is rejected considering two criteria:
    If the new piece is placed over another piece
    Or if less than 95% of the new piece covers the drawing (black pixels)
    :param prev_img: image_processor before placing the new piece
    :param candidate_img: image_processor with the new piece placed
    :param piece_area: area (number of pixels) of the piece placed
    :return: True if the piece is accepted, False otherwise
    """
    accept_ratio_black_covered = .97  # % of total pixels covered that are black
    covered_black_pixels = (candidate_img == 255).sum() - (prev_img == 255).sum()
    black_covered_ratio = covered_black_pixels / piece_area

    return black_covered_ratio > accept_ratio_black_covered

def get_rotation_angle_between_piece_and_figure(piece_corner: Corner, shape_corner: Corner):
    """
    Gives the rotation to give to the piece in order to be aligned with the shape
    :param piece_corner: corner of the piece
    :param shape_corner: corner of the shape
    :return: the rotation angle
    """
    a1 = shape_corner.first_edge.direction.get_angle_with(piece_corner.first_edge.direction)
    a2 = shape_corner.first_edge.direction.get_angle_with(piece_corner.second_edge.direction)
    a3 = shape_corner.second_edge.direction.get_angle_with(piece_corner.first_edge.direction)
    a4 = shape_corner.second_edge.direction.get_angle_with(piece_corner.second_edge.direction)
    return get_duplicate([a1, a2, a3, a4])

def are_two_triangle_corners_on_two_shape_corners(triangle_corners: list[Corner], shape_corners: list[Corner]) -> bool:
    """
    Tells if at least two corners of the triangle are placed on corners of the shape
    :param triangle_corners: corners of the triangle
    :param shape_corners: corners of the shape
    :return: True if it is the case, False otherwise
    """
    close_triangle_corners_from_shape_corners = 0
    triangle_corners_index = 0
    while triangle_corners_index < len(triangle_corners):
        shape_corners_index = 0
        while shape_corners_index < len(shape_corners):
            if triangle_corners[triangle_corners_index].is_close_to(shape_corners[shape_corners_index], 10):
                close_triangle_corners_from_shape_corners += 1
                triangle_corners_index += 1
                break
            shape_corners_index += 1
        triangle_corners_index += 1
    return close_triangle_corners_from_shape_corners > 1

### IMAGE UTILS ###

def show_image(image: np.ndarray) -> None:
    """
    Opens a window to display an image
    :param image: image to display
    """
    cv.imshow("Tangram", image)
    cv.waitKey(0)

def draw_corners_edges_and_angles(image):
    """
    Draws the corners of the shape on the image_processor
    :param image: the image_processor on which we draw the edges
    :return: the image_processor with edges and angles drawn
    """
    result_image = cv.cvtColor(image.copy(), cv.COLOR_GRAY2BGR)
    for corner in get_corners(image):
        result_image = cv.putText(result_image, str(round(corner.angle_between_edges * 10)), (corner.x, corner.y), cv.FONT_HERSHEY_SIMPLEX,
                            .5, (255,0,255), 2, cv.LINE_AA)
        result_image = cv.line(result_image, (corner.first_edge.start_point.x, corner.first_edge.start_point.y),
                        (int(corner.first_edge.direction.get_normalized().x * 20 + corner.first_edge.start_point.x) , int(corner.first_edge.direction.get_normalized().y * 20 + corner.first_edge.start_point.y)),
                        (255,0,0), 2)
        result_image = cv.line(result_image, (corner.second_edge.start_point.x, corner.second_edge.start_point.y),
                        (int(corner.second_edge.direction.get_normalized().x * 20 + corner.second_edge.start_point.x) , int(corner.second_edge.direction.get_normalized().y * 20 + corner.second_edge.start_point.y)),
                        (0,0,255), 2)
    return result_image

def draw_piece_in_image(image: np.ndarray([], dtype=int), piece, color: int | tuple[int, int, int] = 255):
    """
    draws a shape on the image_processor from its vertexes coordinates
    :param image: image_processor we want to draw in
    :param piece: piece to draw
    :param color: color of the piece to draw, white by default
    :return the new matrix of the image_processor with the shape in it
    """
    points = []
    for point in piece.get_points_in_image():
        points.append([point.x, point.y])
    points = np.array(points, np.int32)
    points = points.reshape((-1, 1, 2))
    result_image = cv.fillPoly(image, [points], color)
    return result_image

def is_piece_accepted_at_shape_corner(image: np.ndarray, piece: Piece, shape_corner: Corner) -> (bool, np.ndarray):
    """
    Tells if the piece placement at this corner of the shape is accepted or not
    :param image: image_processor of which we place the piece
    :param piece: piece to place on the image_processor
    :param shape_corner: corner of the shape where we want to place the piece
    :return: True if the placement is correct, False otherwise
    """
    if piece.name == "Large Triangle":  # if the large triangle doesn't touch two corners it can't be correct
        if not are_two_triangle_corners_on_two_shape_corners(piece.get_points_in_image(), get_corners(image)):
            return False, image
    rotation = get_rotation_angle_between_piece_and_figure(piece.corners[0], shape_corner)
    candidate_image = place_piece_in_image_at_point(image, rotation, shape_corner, piece)
    piece_accepted = accept_new_piece(image, candidate_image, piece.area)
    return piece_accepted, candidate_image

def place_piece_in_image_at_point(image: np.ndarray, angle_to_rotate: float, piece: Piece, goal: Point) -> np.ndarray:
    """
    Places the piece on a
    :param image: image_processor on which we want to place the piece
    :param angle_to_rotate: necessary rotation of the piece
    :param piece: piece that we want to place on the image_processor
    :param goal: point on which we want to place the current piece corner
    :return: the image_processor with the piece added on it
    """
    piece.position_in_image = goal
    piece.rotate_shape_around_its_pivot_point(angle_to_rotate)
    candidate_image = draw_piece_in_image(image, piece)
    return candidate_image

def place_all_pieces_on_image(image: np.ndarray, pieces: list[Piece]) -> np.ndarray:
    """
    Places all pieces of a list on an image
    :param image: image on which we want to place the pieces
    :param pieces: list of pieces to place
    :return: the resulting image
    """
    image_rgb =  cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    for piece in pieces:
        draw_piece_in_image(image_rgb, piece, piece.color)
    image_rgb = cv.cvtColor(image_rgb, cv.COLOR_BGR2RGB)
    return image_rgb

def get_corners(image: np.ndarray) -> list[Corner]:
    """
    Gives the coordinates of all the corners of the shape, and all its edges
    :param image: image_processor from which we want the corners and edges
    :return: a list of the corners, which also has the edges in it
    """
    corners = []
    contours = cv.findContours(image, 1, 2)[0]
    for contour in contours[:-1]:  # last contour is the contour of the image_processor
        if cv.contourArea(contour) < MIN_SUB_PUZZLE_AREA:  # if the sub puzzle is too small, skips it
            continue

        sub_puzzle_corners = [Corner(contour[0][0][0], contour[0][0][1])]
        contour_length = len(contour)

        for i in range(1, contour_length):  # gets all the corners
            corner = Corner(contour[i][0][0], contour[i][0][1])
            if not corner.is_close_to(sub_puzzle_corners[-1]):
                sub_puzzle_corners.append(corner)
            else:
                # if too close, changes the last corner to the average of the two
                sub_puzzle_corners[-1] = Corner(int((sub_puzzle_corners[-1].x + corner.x) / 2),
                                                int((sub_puzzle_corners[-1].y + corner.y) / 2))

        if sub_puzzle_corners[0].is_close_to(sub_puzzle_corners[-1]):
            sub_puzzle_corners[0] = Corner(int((sub_puzzle_corners[-1].x + sub_puzzle_corners[0].x) / 2),
                                            int((sub_puzzle_corners[-1].y + sub_puzzle_corners[0].y) / 2))
            sub_puzzle_corners.pop()

        corners_number = len(sub_puzzle_corners)
        for i in range(corners_number):  # link them with edges
            previous_corner = sub_puzzle_corners[i - 1]
            corner = sub_puzzle_corners[i]
            next_corner = sub_puzzle_corners[(i + 1) % corners_number]

            corner.first_edge = Edge(corner, previous_corner)
            corner.second_edge = Edge(corner, next_corner)

            corner.compute_angle_between_edges()

        corners.extend(sub_puzzle_corners)
    return corners
