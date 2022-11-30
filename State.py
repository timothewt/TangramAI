from __future__ import annotations
import cv2 as cv
from copy import deepcopy
from model import ImageProcessor
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

                if self.accept_new_piece(self.image, candidate_image, working_piece.color):
                    new_available_pieces = self.available_pieces.copy()
                    new_available_pieces.pop(self.current_working_piece_index)
                    new_corners = self.corners.copy()
                    new_corners.extend(working_piece.get_points_in_image())
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
                self.current_working_piece_index += 1

        if next_state is None and self.last_piece_placed is not None:
            self.last_piece_placed.corners_visited.append(self.last_piece_placed_corner)

        return next_state

    def next_states(self):
        next_states: list[State] = []
        for i in range(len(self.available_pieces)):
            work_piece: Piece = deepcopy(self.available_pieces[i])
            for placement in self.find_all_piece_placements(work_piece):
                new_available_pieces = self.available_pieces.copy()
                new_available_pieces.pop(i)
                new_corners = deepcopy(self.corners)
                new_corners.extend(placement['pieces_corners'])
                next_states.append(
                    State(
                        available_pieces=new_available_pieces,
                        image=placement['image'],
                        corners=new_corners
                    )
                )
        return next_states

    def find_all_piece_placements(self, piece):  # -> image, corners
        placements = []
        rotations_number = 8
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

    def accept_new_piece(self, prev_img: np.ndarray([], dtype=int), candidate_img: np.ndarray([], dtype=int),
                         color: int) -> bool:
        """
        Says if the placement of the new piece is rejected considering two criteria:
        If the new piece is placed over another piece
        Or if less than 99% of the new piece covers the drawing (black pixels)
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
        if len(node.current_state.available_pieces) == 0:
            print("Found solution!")
            return node
        cv.imshow("Tangram", node.current_state.image)
        cv.waitKey(0)
    return None


if __name__ == "__main__":
    pass
