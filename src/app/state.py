"""
State machine pattern implementation, here we define the base state class
and the enum of all possible states.
"""
from abc import ABC, abstractmethod
from enum import Enum, auto
from src.app.application import Application

class StatesEnum(Enum):
    """
    Enum of all possible states.
    """
    SPLASH = auto()
    SIGNUP = auto()
    LOGIN = auto()
    LOGGOUT = auto()
    MAIN = auto()
    DAYEVENTS = auto()

class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Application object,
    associated with the State. This backreference can be used by States to
    transition the Application to another State.
    """

    def __init__(self, context: Application):
        self.context = context
        self.view = context.ui.view

    @property
    def context(self):
        """
        The State's backreference to the Application.
        """
        return self._context

    @context.setter
    def context(self, context) -> None:
        """
        Setter of the Application's backreference to the State.
        """
        self._context = context

    @abstractmethod
    def render(self) -> None:
        """
        Handle render request.
        """

    def clear(self) -> None:
        """
        Handle clear request.
        """
        self.view.clear_view()

    def transition_to(self, state_enum, **kwargs) -> None:
        """
        The State defines a method for transitioning the Application to
        another State.
        """

        if state_enum == StatesEnum.SPLASH:
            from src.app.state_machine.splash_state import SplashState
            self.context.transition_to(SplashState(self._context, **kwargs))
        elif state_enum == StatesEnum.SIGNUP:
            from src.app.state_machine.sign_up_state import SignUpState
            self.context.transition_to(SignUpState(self._context, **kwargs))
        elif state_enum == StatesEnum.LOGIN:
            from src.app.state_machine.login_state import LoginState
            self.context.transition_to(LoginState(self._context, **kwargs))
        elif state_enum == StatesEnum.LOGGOUT:
            from src.app.state_machine.logging_out_state import LoggingOutState
            self.context.transition_to(LoggingOutState(self._context, **kwargs))
        elif state_enum == StatesEnum.MAIN:
            from src.app.state_machine.main_state import MainState
            self.context.transition_to(MainState(self._context, **kwargs))
        elif state_enum == StatesEnum.DAYEVENTS:
            from src.app.state_machine.day_events_state import DayEventsState
            self.context.transition_to(DayEventsState(self._context, **kwargs))
        else:
            raise ValueError(f"Invalid state: {state_enum}")

    def __str__(self):
        return "Unnammed State"
