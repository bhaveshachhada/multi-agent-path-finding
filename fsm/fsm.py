import sys
import traceback
from threading import Event
from threading import Thread


class FSM(object):
    FSM_STATUS_RUN = 1
    FSM_STATUS_PAUSE = 2

    def __init__(self, name, logger=None):

        self.name = name  # just a name
        self.state_routine_map = {}  # a map which contains a next state (default is current state) and a state_routine
        self.current_state = None  # holds the current state
        self.previous_state = None  # holds the last executed state, used for retry when error.
        self.exit_requested = False  # used to exit the thread
        self.standby = False
        self.current_status = 1
        self.new_requested_state = None
        self.fsm_logger = logger
        self.fsm_thread = None
        self.event = Event()
        self.is_sleeping = False

    def add_state(self, state, default_next_state, routine):
        """
        To Add state into FSM, before add state make sure you define handler function for the same state

        :param state: current state which is running
        :param default_next_state: default state if any thing wrong happened in current state
        :param routine: handler for the current state
        :return: NULL
        """
        self.state_routine_map[state] = (default_next_state, routine)

    def set_current_state(self, state):
        """
        To set state in running FSM

        :param state: which state want to set as current state.
        :return: NULL
        """
        if self.fsm_logger:
            self.fsm_logger.info("Set_current_state=" + str(state) + "logger_name=" + str(self.name))
        self.new_requested_state = state
        if state == 'Standby':
            self.standby = True

    def start_fsm(self, run_only_once=False):
        """
        It will start FSM which is set in default state

        :param run_only_once: If we don't want to run fsm continuously then we set this flag True
        :return: None
        """
        try:
            self.exit_requested = False
            while not self.exit_requested:
                if self.current_status == self.FSM_STATUS_RUN:
                    if not len(self.state_routine_map):
                        # as long as there are some state
                        # the thread is alive
                        break
                    func = self.state_routine_map[self.current_state][1]
                    next_state = func()
                    self.previous_state = self.current_state
                    if self.new_requested_state is None:
                        if next_state is not None:
                            self.current_state = next_state
                        else:
                            self.current_state = self.state_routine_map[self.current_state][0]
                    else:
                        self.current_state = self.new_requested_state
                        self.new_requested_state = None
                else:
                    pass

                if run_only_once:
                    break
        except Exception as ex:
            if self.fsm_logger:
                self.fsm_logger.exception('error in fsm thread execution {ex}'.format(ex=ex))
            traceback.print_exc(file=sys.stdout)

    def stop(self):
        """
        It will stop the FSM

        :return: NULL
        """
        self.exit_requested = True
        self.name = ''

    def stand_by(self):
        """
        To put FSM in stand by mode

        :return: NULL
        """
        pass

    def start_fsm_thread(self):
        self.fsm_thread = Thread(target=self.start_fsm, name=self.name)
        self.fsm_thread.setDaemon(True)
        self.fsm_thread.start()

    def sleep_fsm(self, timeout=None):
        self.event.clear()
        self.is_sleeping = True
        self.event.wait(timeout)
        self.is_sleeping = False

    def wake_up(self):
        self.event.set()
