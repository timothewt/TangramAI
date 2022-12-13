from __future__ import annotations
import cv2 as cv
import numpy as np
from Node import Node
from elements import Piece, Corner


def draw_piece_in_image(image: np.ndarray([], dtype=int), piece, color: int | tuple[int, int, int] = 255):
    """
    draws a shape on the image from its vertexes coordinates
    :param image: image we want to draw in
    :param piece: piece to draw
    :param color: color of the piece to draw, white by default
    :return the new matrix of the image with the shape in it
    """
    points = []
    for point in piece.get_points_in_image():
        points.append([point.x, point.y])
    points = np.array(points, np.int32)
    points = points.reshape((-1, 1, 2))
    result_image = cv.fillPoly(image, [points], color)
    return result_image

def draw_angles_in_image(image : np.ndarray([], dtype=int), color : int | tuple[int, int, int] = (255,0,255), corners : list[Corner] = None) :
    final_img = image.copy()
    final_img = cv.cvtColor(final_img, cv.COLOR_GRAY2BGR)
    length_edges = 50
    for corner in corners:
        final_img = cv.line(final_img, (corner.x, corner.y), (
            int(corner.first_edge.direction.get_normalized().x * length_edges) + corner.x,
            int(corner.first_edge.direction.get_normalized().y * length_edges) + corner.y), (255,0,0), 2)
        final_img = cv.line(final_img, (corner.x, corner.y),
            (int(corner.second_edge.direction.get_normalized().x * length_edges)+ corner.x,
             int(corner.second_edge.direction.get_normalized().y * length_edges)+ corner.y), (0,0,255), 2)
        final_img = cv.circle(final_img, (corner.x, corner.y), 5, (255,255,0), -1)
        final_img = cv.putText(final_img, str(round(corner.angle_between_edges)), (corner.x, corner.y), cv.FONT_HERSHEY_SIMPLEX,
                            1, color, 2, cv.LINE_AA)


    final_img = cv.cvtColor(final_img, cv.COLOR_BGR2RGB)
    return final_img


def approx_eq(a, b):
    return b - 2 < a < b + 2


def search(initial_state) -> Node:  # backtracking
    node = Node(initial_state)
    while node.current_state is not None:
        next_state = node.current_state.get_next_state()
        if next_state is None:
            node = node.previous_node
        else:
            node = Node(current_state=next_state, previous_node=node)

            show_image(next_state.image)
        if node is None:
            return None
        if len(node.current_state.available_pieces) == 0:
            return node
    return None


def reconstruct_solution(image: np.ndarray, pieces: list[Piece]) -> np.ndarray:
    image_rgb =  cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    for piece in pieces:
        draw_piece_in_image(image_rgb, piece, piece.color)
    image_rgb = cv.cvtColor(image_rgb, cv.COLOR_BGR2RGB)
    return image_rgb


def show_image(image):
    cv.imshow("Tangram", image)
    cv.waitKey(0)

def get_duplicate(values: list[float]) -> float:
    result = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if approx_eq(abs(values[i]), 180) and approx_eq(-values[i], values[j]):  # we may have to similar angles like 180 and -180
                result = values[i]
            if approx_eq(values[i], values[j]):
                result = values[i]
    return result
