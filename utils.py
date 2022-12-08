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
    cv.fillPoly(image, [points], color)


def approx_eq(a, b):
    return b * .96 < a < b * 1.04


def search(initial_state) -> Node:  # backtracking
    node = Node(initial_state)
    while node.current_state is not None:
        next_state = node.current_state.get_next_state()
        if next_state is None:
            node = node.previous_node
        else:
            node = Node(current_state=next_state, previous_node=node)
            show_image(node.current_state.image)
        if node is None:
            print("No possible solution.")
            return None
        if len(node.current_state.available_pieces) == 0:
            print("Found solution!")
            return node
    return None


def reconstruct_solution(image: np.ndarray, pieces: list[Piece]) -> np.ndarray:
    image_rgb =  cv.cvtColor(image, cv.COLOR_GRAY2RGB)
    for piece in pieces:
        draw_piece_in_image(image_rgb, piece, piece.color)
    return image_rgb


def show_image(image):
    cv.imshow("Tangram", image)
    cv.waitKey(0)
