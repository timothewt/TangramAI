from __future__ import annotations
import cv2 as cv
from copy import deepcopy

from ImageProcessor import show_image
from elements import *


class State:
    def __init__(self, available_pieces, image, corners, last_piece_placed=None, last_piece_placed_corner=None):
        self.available_pieces: list[Piece] = available_pieces.copy()
        self.working_pieces: list[Piece] = deepcopy(available_pieces)
        self.current_working_piece_index: int = 0
        self.corners: list[Point] = corners
        self.current_corner_index: int = 0
        self.image: np.ndarray(int) = image.copy()
        self.last_piece_placed: Piece = last_piece_placed
        self.last_piece_placed_corner: Point = last_piece_placed_corner

    def get_next_state(self):
        next_state = None
        while next_state is None and self.current_working_piece_index < len(self.working_pieces):
            if self.working_pieces[0].name == "Large Triangle" and self.current_working_piece_index > 0:  # if the large triangles are not placed we can't go further
                return None
            working_piece = self.working_pieces[self.current_working_piece_index]

            if self.corners[self.current_corner_index] not in working_piece.corners_visited:
                working_piece.position_in_image = self.corners[self.current_corner_index]
                candidate_image = self.image.copy()
                self.draw_shape_on_image(candidate_image, working_piece)
                if self.accept_new_piece(self.image, candidate_image, working_piece.area):
                    new_available_pieces = self.available_pieces.copy()
                    new_available_pieces.pop(self.current_working_piece_index)
                    new_corners = self.corners.copy()
                    new_corners.extend(working_piece.get_points_in_image())
                    show_image(candidate_image)
                    next_state = State(
                        available_pieces=new_available_pieces,
                        image=candidate_image,
                        corners=new_corners,
                        last_piece_placed=self.available_pieces[self.current_working_piece_index],
                        last_piece_placed_corner=self.corners[self.current_corner_index]
                    )

                working_piece.rotate_shape_around_pivot(45)

                if working_piece.rotation >= 360:
                    self.current_corner_index += 1
                    working_piece.rotation = 0
            else:
                self.current_corner_index += 1

            if self.current_corner_index >= len(self.corners):
                self.current_corner_index = 0
                if self.working_pieces[self.current_working_piece_index].name == "Parallelogram" and not self.working_pieces[self.current_working_piece_index].is_flipped:
                    self.working_pieces[self.current_working_piece_index].flip()
                else:
                    self.current_working_piece_index += 1

        if next_state is None and self.last_piece_placed is not None:
            self.last_piece_placed.corners_visited.append(self.last_piece_placed_corner)

        return next_state

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
        cv.fillPoly(image, [points], 255)

    def accept_new_piece(self, prev_img: np.ndarray([], dtype=int), candidate_img: np.ndarray([], dtype=int),
                         piece_area: int) -> bool:
        """
        Says if the placement of the new piece is rejected considering two criteria:
        If the new piece is placed over another piece
        Or if less than 97% of the new piece covers the drawing (black pixels)
        :param prev_img: image before placing the new piece
        :param candidate_img: image with the new piece placed
        :param piece_area: area (number of pixels) of the piece placed
        :return: True if the piece is accepted, False otherwise
        """
        accept_ratio_black_covered = .97  # % of total pixels covered that are black
        covered_black_pixels = (candidate_img == 255).sum() - (prev_img == 255).sum()
        black_covered_ratio = covered_black_pixels / piece_area

        return black_covered_ratio > accept_ratio_black_covered


class Node:
    def __init__(self, current_state: State, previous_node: Node = None):
        self.current_state = current_state
        self.previous_node = previous_node


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


if __name__ == "__main__":
    pass
