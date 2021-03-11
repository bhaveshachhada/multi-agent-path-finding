from src.utility import load_json
from collections import defaultdict
from design_patterns.singleton import Singleton


class Layout(Singleton):

    def __init__(self):

        Singleton.__init__(self)

        self.graph_file = "data/graph.json"
        self.graph = self.load_graph()

        # note: used to block a node by an agent
        self.block_node_map = defaultdict(lambda: None)

        # note: node can be used for navigation by other agents but can't be set as destination by other agents
        self.semi_block_node_map = defaultdict(lambda: None)
        self.semi_block_node_queue = defaultdict(list)

    def load_graph(self):
        return load_json(self.graph_file)

    def block_node(self, node, agent_id):
        if self.block_node_map[node] is None:
            self.block_node_map[node] = agent_id

    def unblock_node(self, node):
        self.block_node_map[node] = None

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

        self.solver = path_finder(planner=self)
        self.agents = list()
        self.agent_position_map = dict()
        self.agent_destination_map = dict()

        self.layout_manager = Layout.get_instance()

    def add_agent(self, agent, position):
        if agent not in self.agents:
            self.agents.append(agent)
            self.agent_position_map[agent.id] = position
            self.layout_manager.block_node(node=position, agent_id=agent.id)

    def get_agent_location(self, agent_id):
        return self.agent_position_map[agent_id]

    def update_agent_location(self, agent_id, position):
        old_location = self.agent_position_map[agent_id]
        self.layout_manager.unblock_node(node=old_location)
        self.agent_position_map[agent_id] = position

    def find_path(self):

        pass
