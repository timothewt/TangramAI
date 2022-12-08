from __future__ import annotations


class Node:
    def __init__(self, current_state, previous_node: Node = None):
        self.current_state = current_state
        self.previous_node = previous_node
