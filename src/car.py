from src.agent import Agent
from logging_module.logging_module import setup_logger


class Car(Agent):

    def __init__(self, agent_id=None, name='', current_position=None):

        Agent.__init__(self, agent_id=agent_id, name=name, current_position=current_position)

        logger_name = f'{self.__class__.__name__}-{self.id}'
        self.logger = setup_logger(logger_name)

    @property
    def current_position(self):
        return self._current_position

    @current_position.setter
    def current_position(self, position):
        if type(position) == str:
            position = self.planner.get_node(node=position)
        self.logger.info(f'current_position: {self._current_position}')
        self._current_position = position

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, position):
        if type(position) == str:
            position = self.planner.get_node(node=position)
        self._destination = position
        self.logger.info(f'destination: {self._destination}')

    @property
    def reached(self):
        return self._reached

    @reached.setter
    def reached(self, data):
        self._reached = data

    def go_to_position(self, destination=None):
        pass

    def make_movement(self, move):
        pass

    def provide_actions(self, actions: list):
        pass
