from threading import Lock

from algorithms.path_finder import PathFinder
from data_structures.locked_defaultdict import LockedDefaultDict
# from collections import defaultdict
from design_patterns.singleton import Singleton
from logging_module.logging_module import setup_logger
from src.node import Node
from src.utility import load_json

MIN_COST = -10000


class Planner(Singleton):

    def __init__(self, path_finder: PathFinder = None):

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
