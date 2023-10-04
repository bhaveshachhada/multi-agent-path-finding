from typing import List, Set, Tuple, Dict

from algorithms.path_finder import PathFinder
from src.node import Node
from src.path import Path


class BreadthFirstSearch(PathFinder):

    def find_path(self, source: Node, destination: Node) -> Tuple[bool, Path]:

        current_node: Node = source

        if current_node == destination:
            return True, Path([], cost=0)

        elif destination in current_node.connected_nodes:
            return True, Path([destination], cost=1)

        else:

            parent: Dict[Node, Node] = dict()

            # start with a fringe set consisting only the nodes adjacent to source node
            fringe_set: List[Node] = list()
            for neighbour in source.connected_nodes:
                fringe_set.append(neighbour)
                parent[neighbour] = source

            visited_set: Set[Node] = {source}  # source is visited and checked already

            path: List[Node] = list()

            while fringe_set:

                current_node = fringe_set.pop(0)

                if current_node == destination:
                    # todo: construct path backwards to source
                    path.append(destination)
                    node = destination
                    while parent[node] != source:
                        path.append(node)
                        node = parent[node]
                    path.append(node)
                    path = list(reversed(path))
                    return True, Path(nodes=path, cost=len(path))

                else:

                    visited_set.add(current_node)

                    neighbours = current_node.connected_nodes

                    for neighbour in neighbours:

                        if neighbour not in visited_set:
                            parent[neighbour] = current_node
                            fringe_set.append(neighbour)

            return False, Path([])
