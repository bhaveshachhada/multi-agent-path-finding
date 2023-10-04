from typing import List

from data_structures.locked_defaultdict import LockedDefaultDict


class Node:

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.position = data['pos']
        self.rfid = data['rf_id']
        self._agent = None
        self._blocked = False
        self.connected_nodes_map = LockedDefaultDict(lambda x: None)
        self.connected_nodes: List['Node'] = list()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def agent(self):
        return self._agent

    @agent.setter
    def agent(self, agent_id):
        self._agent = agent_id

    @property
    def blocked(self):
        return self._blocked

    @blocked.setter
    def blocked(self, data):
        self._blocked = data

    def add_neighbour(self, node, direction):
        self.connected_nodes_map[direction] = node
        self.connected_nodes.append(node)

    def get_neighbour(self, direction):
        return self.connected_nodes_map[direction]

    def block(self, agent_id):
        self.agent = agent_id
        self.blocked = True

    def unblock(self):
        agent_id = self.agent
        self.agent = None
        self.blocked = False
        return agent_id