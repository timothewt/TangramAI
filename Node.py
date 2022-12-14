from __future__ import annotations


class Node:
    """
    Used to track the current and previous states of the puzzle

    Attributes:
        current_state:  current state of the puzzle
        previous_node:  node containing the previous state of the puzzle
    """
    def __init__(self, current_state, previous_node: Node = None):
        self.current_state = current_state
        self.previous_node = previous_node
