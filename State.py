import numpy as np
import cv2 as cv
from copy import deepcopy
from model import TangramSolver
from elements import *


class State:
    def __init__(self, available_pieces=None, placed_pieces=None, image=None, corners=None):
        self.available_pieces: list[Piece] = available_pieces
        self.placed_pieces: list[Piece] = placed_pieces
        self.image: np.ndarray(int) = image.copy()
        self.corners: list[Point] = corners

    def next_states(self):
        next_states: list[State] = []
        for i in range(len(self.available_pieces)):
            work_piece: Piece = deepcopy(self.available_pieces[i])
            for placement in self.find_all_piece_placements(work_piece):
                cv.imshow("Tangram", placement['image'])
                cv.waitKey(0)
                new_available_pieces = deepcopy(self.available_pieces)
                new_available_pieces.pop(i)
                new_corners = deepcopy(self.corners)
                new_corners.extend(placement['pieces_corners'])
                new_placed_pieces = deepcopy(self.placed_pieces)
                new_placed_pieces.append(deepcopy(self.available_pieces[i]))
                next_states.append(
                    State(
                        available_pieces=new_available_pieces,
                        placed_pieces=new_placed_pieces,
                        image=placement['image'],
                        corners=new_corners
                    )
                )
        return next_states

    def find_all_piece_placements(self, piece):  # -> image, corners
        placements = []
        rotations_number = 12
        for corner in self.corners:
            piece.position_in_image = corner
            for _ in range(rotations_number):
                candidate_image = self.image.copy()
                self.draw_shape_on_image(candidate_image, piece)
                if self.accept_new_piece(self.image, candidate_image, piece.color):
                    placements.append({
                        'image': candidate_image,
                        'pieces_corners': piece.get_points_in_image()
                    })
                piece.rotate_shape_around_pivot(360 // rotations_number)
        return placements

    def draw_shape_on_image(self, image: np.ndarray([], dtype=int), piece):
        """
        draws a shape on the image from its vertexes coordinates
        :param image: image we want to draw in
        :param piece: piece to draw
        :return the new matrix of the image with the shape in it
        """
        points = []
        for point in piece.get_points_in_image():
            points.append([point.x, point.y])
        points = np.array(points, np.int32)
        points = points.reshape((-1, 1, 2))
        cv.fillPoly(image, [points], piece.color)

    def accept_new_piece(self, prev_img: np.ndarray([], dtype=int), candidate_img: np.ndarray([], dtype=int), color: int) -> bool:
        """
        Says if the placement of the new piece is rejected considering two criteria:
        If the new piece is placed over another piece
        Or if less than 97% of the new piece covers the drawing (black pixels)
        :param prev_img: image before placing the new piece
        :param candidate_img: image with the new piece placed
        :return: True if the piece is rejected, False otherwise
        """
        accept_ratio = .97
        covered_black_pixels = (prev_img == 0).sum() - (candidate_img == 0).sum()
        covered_non_black_pixels = (candidate_img == color).sum() - covered_black_pixels
        if covered_black_pixels == 0 and covered_non_black_pixels == 0:
            return False
        non_black_covered_ratio = covered_black_pixels / (covered_non_black_pixels + covered_black_pixels)
        return non_black_covered_ratio > accept_ratio


class Node:
    def __init__(self, current_state, previous_state=None):
        self.current_state = current_state
        self.previous_state = previous_state


def search(initial_state) -> Node:
    nodes = [Node(initial_state)]
    while len(nodes) > 0:
        node = nodes.pop(0)
        if len(node.current_state.available_pieces) == 0:
            return node
        new_nodes = [Node(state, node) for state in node.current_state.next_states()]
        new_nodes.extend(nodes)  # we put the new nodes at the top of the stack
        nodes = new_nodes
    return None


if __name__ == "__main__":
    ai_tangram = TangramSolver('tangram_unsolved.png')
    av_pieces = [
        LargeTriangle(32),
        LargeTriangle(64),
        Parallelogram(96),
        Square(128),
        MediumTriangle(160),
        SmallTriangle(192),
        SmallTriangle(224),
    ]

    root_state = State(av_pieces, [], ai_tangram.image, ai_tangram.corners)
    search(root_state)
