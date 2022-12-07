from __future__ import annotations
import cv2 as cv
from copy import deepcopy

from ImageProcessor import ImageProcessor, show_image
from elements import *


class State:
    def __init__(self, available_pieces, image, corners, used_pieces=None, last_piece_placed=None,
                 last_piece_placed_corner=None):
        self.available_pieces: list[Piece] = available_pieces.copy()
        self.working_pieces: list[Piece] = deepcopy(available_pieces)
        if used_pieces is None:
            used_pieces = []
        self.used_pieces: list[Piece] = used_pieces
        self.current_working_piece_index: int = 0
        self.corners: list[Corner] = corners
        self.current_corner_index: int = 0
        self.image: np.ndarray = image.copy()
        self.last_piece_placed: Piece = last_piece_placed
        self.last_piece_placed_corner: Point = last_piece_placed_corner
        self.image_processor = ImageProcessor()

    def get_next_state(self):
        next_state = None
        while next_state is None and self.current_working_piece_index < len(self.working_pieces):
            working_piece = self.working_pieces[self.current_working_piece_index]
            print("Trying", working_piece.name, "at corner n°", self.current_corner_index)
            # Check for every corner of the piece if the angle match a shadow's corner:
            piece_corner = working_piece.corners[0]
            shape_corner = self.corners[self.current_corner_index]
            piece_corner.compute_angle_between_edges()
            print("Angle piece :" + str(piece_corner.angle_between_edges))
            print("Angle shadow " + str(shape_corner.angle_between_edges))
            if approx_eq(self.corners[self.current_corner_index].angle_between_edges, piece_corner.angle_between_edges):
                print("Angle match")

                # First Edge
                angle_to_rotate = shape_corner.first_edge.direction.get_angle_with(piece_corner.first_edge.direction)
                # Rotate the piece to align to edges
                candidate_image = self.try_piece_in_image(angle_to_rotate, shape_corner, working_piece)

                if self.accept_new_piece(self.image, candidate_image, working_piece.area):
                    print("Placed", working_piece.name)
                    next_state = self.create_next_state(candidate_image, working_piece)
                    break
                # Second edge
                angle_to_rotate = shape_corner.second_edge.direction.get_angle_with(piece_corner.first_edge.direction)
                # Rotate the piece to align to edges
                candidate_image = self.try_piece_in_image(angle_to_rotate, shape_corner, working_piece)
                if self.accept_new_piece(self.image, candidate_image, working_piece.area):
                    print("Placed", working_piece.name)
                    next_state = self.create_next_state(candidate_image, working_piece)
                    break

            working_piece.next_corner()

            if working_piece.number_of_corner_swap % working_piece.max_corner_swap == 0:
                if working_piece.name == "Parallelogram" and not working_piece.is_flipped:
                    working_piece.flip()
                else:
                    if working_piece.name == "Parallelogram" and working_piece.is_flipped:
                        working_piece.flip()
                    self.current_corner_index += 1

            # If no more corner, try the next piece
            if self.current_corner_index >= len(self.corners):
                self.current_corner_index = 0
                self.current_working_piece_index += 1

        return next_state

    def try_piece_in_image(self, angle_to_rotate, shape_corner, working_piece):
        working_piece.position_in_image = shape_corner
        working_piece.rotate_shape_around_pivot(angle_to_rotate)
        candidate_image = self.image.copy()
        self.draw_piece_in_image(candidate_image, working_piece)
        working_piece.reset_rotation()
        show_image(candidate_image)
        return candidate_image

    def create_next_state(self, candidate_image, working_piece):
        new_available_pieces = self.available_pieces.copy()
        new_available_pieces.pop(self.current_working_piece_index)
        new_used_pieces = self.used_pieces.copy()
        new_used_pieces.append(deepcopy(working_piece))
        new_corners = self.image_processor.get_corners(candidate_image)
        return State(
            available_pieces=new_available_pieces,
            image=candidate_image,
            corners=new_corners,
            used_pieces=self.used_pieces,
            last_piece_placed=self.available_pieces[self.current_working_piece_index],
            last_piece_placed_corner=self.corners[self.current_corner_index]
        )

    def draw_piece_in_image(self, image: np.ndarray([], dtype=int), piece):
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
        Or if less than 95% of the new piece covers the drawing (black pixels)
        :param prev_img: image before placing the new piece
        :param candidate_img: image with the new piece placed
        :param piece_area: area (number of pixels) of the piece placed
        :return: True if the piece is accepted, False otherwise
        """
        accept_ratio_black_covered = .95  # % of total pixels covered that are black
        covered_black_pixels = (candidate_img == 255).sum() - (prev_img == 255).sum()
        black_covered_ratio = covered_black_pixels / piece_area

        return black_covered_ratio > accept_ratio_black_covered


class Node:
    def __init__(self, current_state: State, previous_node: Node = None):
        self.current_state = current_state
        self.previous_node = previous_node


def approx_eq(a, b):
    return b * .98 < a < b * 1.02


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
