import time
from fsm.fsm import FSM
from threading import Event
from src.agent import Agent
from enum import Enum, unique
from logging_module.logging_module import setup_logger


@unique
class CarState(Enum):
    IDLE = 1
    FIND_DIRECTION = 2
    MOVE = 3


class Car(Agent, FSM):

    def __init__(self, agent_id=None, name='', current_position=None):

        Agent.__init__(self, agent_id=agent_id, name=name, current_position=current_position)
        FSM.__init__(name=f'agent:{agent_id}&{name}')

        logger_name = f'{self.__class__.__name__}-{self.id}'
        self.logger = setup_logger(logger_name)

        self.add_fsm_states()
        self.current_state = CarState.IDLE

    def add_fsm_states(self):
        self.add_state(state=CarState.IDLE, default_next_state=CarState.IDLE, routine=self.handler_idle)
        self.add_state(state=CarState.MOVE, default_next_state=CarState.MOVE, routine=self.handler_move)
        self.add_state(state=CarState.FIND_DIRECTION, default_next_state=CarState.FIND_DIRECTION,
                       routine=self.handler_find_direction)

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

    def handler_idle(self):
        self.logger.info(f'In state: {self.current_state.name}')
        pass

    def handler_find_direction(self):
        self.logger.info(f'In state: {self.current_state.name}')
        pass

    def handler_move(self):
        self.logger.info(f'In state: {self.current_state.name}')
        pass
