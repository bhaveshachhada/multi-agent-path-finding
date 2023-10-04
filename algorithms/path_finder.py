from typing import Tuple

from src.node import Node
from src.path import Path


class PathFinder:

    def __init__(self, planner=None):
        self.planner = planner

    def find_path(self, source: Node, destination: Node) -> Tuple[bool, Path]:
        raise Exception("Not implemented")
