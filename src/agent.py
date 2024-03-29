from src.planner import Planner


class Agent:

    def __init__(self, agent_id=None, name='', current_position=None):

        self.id = agent_id
        self.name = name

        self.planner = Planner.get_instance()

        self._current_position = self.planner.get_node(node=current_position)
        self._destination = None
        self._reached = False

        self.actions_to_be_taken = list()

    @property
    def current_position(self):
        return self._current_position

    @current_position.setter
    def current_position(self, position):
        self._current_position = position

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, position):
        self._destination = position

    @property
    def reached(self):
        return self._reached

    @reached.setter
    def reached(self, data):
        self._reached = data

    def go_to_position(self, destination=None):
        raise NotImplementedError(f'Override this method in {self.__class__.__name__} class')

    def provide_actions(self, actions: list):
        raise NotImplementedError(f'Override this method in {self.__class__.__name__} class')

    def make_movement(self, move):
        raise NotImplementedError(f'Override this method in {self.__class__.__name__} class')
