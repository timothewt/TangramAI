from __future__ import annotations
from copy import deepcopy

from ImageProcessor import ImageProcessor
from elements import *
from utils import *


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
            # Check for every corner of the piece if the angle match a shadow's corner:
            piece_corner = working_piece.corners[0]
            shape_corner = self.corners[self.current_corner_index]

            if approx_eq(abs(self.corners[self.current_corner_index].angle_between_edges), abs(piece_corner.angle_between_edges)):
                # First Edge
                a1 = shape_corner.first_edge.direction.get_angle_with(piece_corner.first_edge.direction)
                a2 = shape_corner.first_edge.direction.get_angle_with(piece_corner.second_edge.direction)
                a3 = shape_corner.second_edge.direction.get_angle_with(piece_corner.first_edge.direction)
                a4 = shape_corner.second_edge.direction.get_angle_with(piece_corner.second_edge.direction)

                angle_to_rotate = get_duplicate([a1, a2, a3, a4])

                # Rotate the piece to align to edges
                candidate_image = self.try_piece_in_image(angle_to_rotate, shape_corner, working_piece)

                if self.accept_new_piece(self.image, candidate_image, working_piece.area):
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
        candidate_image = self.image.copy()
        working_piece.rotate_shape_around_pivot(angle_to_rotate)
        candidate_image = draw_piece_in_image(candidate_image, working_piece)
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
            used_pieces=new_used_pieces,
            last_piece_placed=self.available_pieces[self.current_working_piece_index],
            last_piece_placed_corner=self.corners[self.current_corner_index]
        )

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


if __name__ == "__main__":
    pass
