from src.planner import Planner


class Agent:

    def __init__(self, agent_id=None, name='', current_position=None):

        self.id = agent_id
        self.name = name

        self.planner = Planner.get_instance()

        self._current_position = current_position
        self._destination = None

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

    def go_to_position(self, destination=None):
        self.destination = destination

    def provide_actions(self, actions: list):
        self.actions_to_be_taken.extend(actions)


class Car(Agent):

    def __init__(self, agent_id=None, name='', current_position=None):
        Agent.__init__(self, agent_id=agent_id, name=name, current_position=current_position)
        pass
