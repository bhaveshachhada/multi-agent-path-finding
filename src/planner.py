from threading import Lock

from data_structures.locked_defaultdict import LockedDefaultDict
# from collections import defaultdict
from design_patterns.singleton import Singleton
from logging_module.logging_module import setup_logger
from src.node import Node
from src.utility import load_json

MIN_COST = -10000


class Layout(Singleton):

    def __init__(self):

        Singleton.__init__(self)

        self.graph_file = "data/graph.json"
        self.graph = self.load_graph()

        self.logger = setup_logger('graph')

        # note: used to block a node by an agent
        self.block_node_map = LockedDefaultDict(lambda: None)

        # note: node can be used for navigation by other agents but can't be set as destination by other agents
        self.semi_block_node_map = LockedDefaultDict(lambda: None)

        # note: added for future use, currently experiment without semi block
        self.semi_block_node_queue = LockedDefaultDict(list)

    def load_graph(self):
        return load_json(self.graph_file)

    def block_node(self, node, agent_id):
        if self.block_node_map[node] is None:
            self.block_node_map[node] = agent_id
            self.logger.info(f'{node} blocked by {agent_id}')
        else:
            self.logger.info(f'{node} cannot be blocked by {agent_id}, {self.block_node_map[node]} has blocked')

    def unblock_node(self, node):
        # self.block_node_map[node] = None
        agent_id = self.block_node_map.pop(node)
        self.logger.info(f'{node} unblocked by {agent_id}')

    def is_node_free(self, node):
        return self.block_node_map[node] is None

    def is_node_blocked_for_agent(self, node, agent_id):
        return self.block_node_map[node] != agent_id

    def is_node_blocked_by_agent(self, node, agent_id):
        return self.block_node_map[node] == agent_id

    def semi_block_enable(self, node):
        agent_id = self.semi_block_node_queue[node][0]
        self.semi_block_node_map[node] = agent_id

    def semi_block_disable(self, node):
        self.semi_block_node_queue[node].pop(0)
        self.semi_block_node_map.pop(node)

    def request_semi_block(self, node, agent_id):
        if agent_id not in self.semi_block_node_queue[node]:
            self.semi_block_node_queue[node].append(agent_id)
            if len(self.semi_block_node_queue[node]) == 1:
                self.semi_block_enable(node=node)

    def withdraw_semi_block(self, node):
        self.semi_block_disable(node=node)


class Planner(Singleton):

    def __init__(self, path_finder=None):

        Singleton.__init__(self)

        self.solver = path_finder  # (planner=self)
        self.logger = setup_logger('planner')

        self.agents = list()
        self.agent_position_map = dict()
        self.agent_destination_map = dict()
        self.block_node_lock = Lock()

        self.graph_file = "data/graph.json"
        self.graph = self.load_graph()
        self.node_object_map = LockedDefaultDict(lambda x: None)
        self.setup_nodes()

    def load_graph(self):
        return load_json(self.graph_file)

    def setup_nodes(self):
        for node in self.graph:
            data = self.graph[node]
            node_instance = Node(name=node, data=data)
            self.node_object_map[node] = node_instance
            self.logger.info(f'setup node: {node}')
        for node, node_instance in self.node_object_map.items():
            adjacent_nodes = self.graph[node]["connected_node"]
            for adjacent_node in adjacent_nodes:
                adjacent_node_instance = self.node_object_map[adjacent_node]
                direction = self.graph[node]["direction"][adjacent_node]
                node_instance.add_neighbour(node=adjacent_node_instance, direction=direction)
                self.logger.info(f'added relation {node} - {direction} - {adjacent_node}')
        self.logger.info(f'setup nodes complete')

    def get_node(self, node=None):
        assert node is not None
        return self.node_object_map[node]

    def block_node(self, node, agent):
        self.block_node_lock.acquire()
        try:
            node_instance: Node = self.node_object_map[node]
            if node_instance.blocked:
                self.logger.info(f'{node} already blocked by {node_instance.agent}')
            else:
                node_instance.block(agent_id=agent.id)
                self.logger.info(f'{node} block by {agent.id}')
        except Exception as e:
            self.logger.exception(f'error in block node: {node} by agent: {agent}, error: {e}')
        finally:
            self.block_node_lock.release()

    def unblock_node(self, node):
        self.block_node_lock.acquire()
        try:
            node_instance: Node = self.node_object_map[node]
            if not node_instance.blocked:
                self.logger.info(f'{node} already unblocked')
            else:
                agent_id = node_instance.unblock()
                self.logger.info(f'{node} unblocked by {agent_id}')
        except Exception as e:
            self.logger.exception(f'error in unblock node: {node}, error: {e}')
        finally:
            self.block_node_lock.release()

    def add_agent(self, agent):
        if agent not in self.agents:
            self.agents.append(agent)
            self.agent_position_map[agent.id] = agent.current_position
            # self.block_node(node=agent.current_position, agent_id=agent.id)
            self.block_node(node=agent.current_position, agent=agent)
            self.logger.info(f'registered agent: {agent.id} at {agent.current_position}')
        else:
            self.logger.info(f'{agent.id} is already registered')

    def remove_agent(self, agent):
        if agent in self.agents:
            self.agent_position_map.pop(agent.id)
            self.unblock_node(agent.current_position)
            self.agents.remove(agent)
            self.logger.info(f'{agent.id} unregistered at {agent.current_position}')
        else:
            self.logger.info(f'cannot remove agent {agent.id}, not registered')

    def get_agent_location(self, agent_id):
        return self.agent_position_map[agent_id]

    def update_agent_location(self, agent_id, position):
        old_location = self.agent_position_map[agent_id]
        self.unblock_node(node=old_location)
        self.agent_position_map[agent_id] = position

    def find_path(self):
        pass

    def best_first_search(self, source, destination):
        pass


if __name__ == '__main__':
    Planner()
