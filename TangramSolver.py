import numpy as np
from State import State
from Node import Node
from elements import *


class TangramSolver:
    """
    Used to solve the tangram puzzle, given the black and white image of the shape

    Attributes:
        puzzle_shadow:  black and white image of the shape to solve
        solution_node:  solution of the puzzle
    """
    def __init__(self, puzzle_shadow: np.ndarray):
        self.puzzle_shadow = puzzle_shadow
        self.solution_node = self.solve_tangram()

    def solve_tangram(self):
        """
        Solves the tangram puzzle using backtracking
        :return: the solution node, if a solution exists, else None
        """
        available_pieces = [
            LargeTriangle((8, 189, 100)),
            LargeTriangle((255, 200, 3)),
            Square((255, 74, 74)),
            MediumTriangle((142, 207, 33)),
            Parallelogram((96, 107, 217)),
            SmallTriangle((44, 174, 242)),
            SmallTriangle((251, 140, 50)),
        ]
        root_state = State(available_pieces, self.puzzle_shadow)
        node = Node(root_state)
        while node.current_state is not None:
            next_state = node.current_state.get_next_state()
            if next_state is None:  # the program cannot place any more piece with this configuration
                node = node.previous_node
            else:
                node = Node(current_state=next_state, previous_node=node)
            if node is None:
                return None
            if len(node.current_state.available_pieces) == 0:
                return node
        return None