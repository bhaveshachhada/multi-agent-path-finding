from typing import List

from src.node import Node


class Path:

    def __init__(self, nodes: List[Node], cost: int = -1):
        self._nodes: List[Node] = nodes
        self._cost: int = cost

    def __str__(self) -> str:
        return f'Path: {self._nodes}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(nodes={self.nodes}, cost={self.cost})'

    def __len__(self) -> int:
        return len(self._nodes)

    def __eq__(self, other: 'Path') -> bool:
        if self.__len__() == len(other):
            for node_a, node_b in zip(self._nodes, other.nodes):
                if node_a != node_b:
                    return False
            return True
        return False

    def __bool__(self):
        return bool(self.available)

    def append(self, path: 'Path') -> None:
        self._nodes.extend(path.nodes)

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, data):
        self._cost = data

    @property
    def nodes(self):
        return self._nodes

    @property
    def available(self):
        return len(self._nodes)

    def clear(self):
        self._nodes.clear()

    # def block(self, car_id, index=0):
    #     global_lock.acquire()
    #     flag = all([not node.is_blocked_for_car(car_id=car_id) for node in self._nodes[index:]])
    #     if flag:
    #         for node in self._nodes[index:]:
    #             node.block(car_id=car_id)
    #     global_lock.release()
    #     return flag

    def get_next_node(self) -> Node:
        if len(self._nodes) >= 1:
            return self._nodes[0]
        return None

    def reached_first_node(self):
        self._nodes.pop(0)
