from __future__ import annotations
import cv2 as cv
import numpy as np
from Node import Node
from elements import Piece


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
