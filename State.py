from __future__ import annotations
from copy import deepcopy
from utils import *


class State:
    """
    Used to represent the current state of the puzzle, i.e. the current pieces' configuration.

    Attributes:
        available_pieces:            All the pieces remaining to complete the puzzle
        working_pieces:              Used to store the pieces that we move, so the available_pieces one stay at the origin
        used_pieces:                 Pieces already placed in this configuration, used to reconstruct the solution
        current_working_piece_index: Index of the piece we are currently trying to place of the puzzle
        current_corner_index:        Index of the corner on which we are trying to place the current working piece
        image:                       Image of the current puzzle configuration
        corners:                     List of the corners of the image_processor
    """
    def __init__(self, available_pieces, image, used_pieces=None):
        self.available_pieces: list[Piece] = available_pieces
        self.working_pieces: list[Piece] = deepcopy(available_pieces)
        self.used_pieces: list[Piece] = used_pieces if used_pieces is not None else []
        self.current_working_piece_index: int = 0
        self.current_corner_index: int = 0
        self.image: np.ndarray = image
        self.corners: list[Corner] = get_corners(self.image)

    def get_next_state(self) -> State:
        """
        Gets the next state of the current puzzle by placing a new piece on the image_processor.
        :return: a new State if another piece can be placed on the current puzzle configuration, None otherwise
        """
        next_state = None

        while next_state is None and self.current_working_piece_index < len(self.working_pieces):
            working_piece = self.working_pieces[self.current_working_piece_index]
            shape_corner = self.corners[self.current_corner_index]

            if approx_eq(abs(shape_corner.angle_between_edges), abs(working_piece.corners[0].angle_between_edges)):
                is_piece_accepted, candidate_image = is_piece_accepted_at_shape_corner(self.image.copy(), working_piece, shape_corner)

                if is_piece_accepted:
                    next_state = self.generate_next_state(candidate_image, working_piece)

            working_piece.shift_corners()

            if working_piece.corners_shifts_counter % working_piece.max_corners_shifts == 0:
                if working_piece.name == "Parallelogram" and not working_piece.is_flipped:
                    working_piece.flip()
                else:
                    if working_piece.name == "Parallelogram" and working_piece.is_flipped:
                        working_piece.flip()
                    self.current_corner_index += 1

            if self.current_corner_index >= len(self.corners):
                self.current_corner_index = 0
                self.current_working_piece_index += 1

        return next_state

    def generate_next_state(self, image: np.ndarray, piece_placed: Piece) -> State:
        """
        Used to pass by value the new state attributes
        :param image: image_processor with the new piece placed
        :param piece_placed: piece placed
        :return: the new State
        """
        new_available_pieces = self.available_pieces.copy()
        new_available_pieces.pop(self.current_working_piece_index)
        new_used_pieces = self.used_pieces.copy()
        new_used_pieces.append(deepcopy(piece_placed))
        return State(
            available_pieces=new_available_pieces,
            image=image,
            used_pieces=new_used_pieces
        )


if __name__ == "__main__":
    pass
