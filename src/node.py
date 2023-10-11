import threading
import traceback
from collections import defaultdict
from functools import wraps
from typing import List, Callable, Dict


class Node:

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.position = data['pos']
        self._agent_id: int = None
        self._blocked: bool = False
        self.connected_nodes_map: Dict[str, 'Node'] = defaultdict(lambda: None)
        self.connected_nodes: List['Node'] = list()
        self.lock = threading.RLock()

    @staticmethod
    def thread_safe(function: Callable):

        @wraps(function)
        def inner(self, *args, **kwargs):

            output = None
            try:
                self.lock.acquire()
                output = function(self, *args, **kwargs)
            except Exception as e:
                print(f'Error while executing {function.__name__}: {e}')
                print(traceback.format_exc())
            finally:
                self.lock.release()
                return output

        return inner

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def agent(self):
        return self._agent_id

    @agent.setter
    def agent(self, agent_id):
        self._agent_id = agent_id

    @property
    def blocked(self):
        return self._blocked

    @blocked.setter
    def blocked(self, data):
        self._blocked = data

    @thread_safe
    def add_neighbour(self, node, direction):
        self.connected_nodes_map[direction] = node
        self.connected_nodes.append(node)

    @thread_safe
    def get_neighbour(self, direction):
        return self.connected_nodes_map[direction]

    @thread_safe
    def block(self, agent_id):
        self.agent = agent_id
        self.blocked = True

    @thread_safe
    def unblock(self):
        agent_id = self.agent
        self.agent = None
        self.blocked = False
        return agent_id
