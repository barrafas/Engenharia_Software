"""
Transition to this state when the user is logging out.
"""
from src.app.state import State, StatesEnum

class LoggingOutState(State):
    """
    Transition to this state when the user is logging out.
    """
    def render(self):
        print("Logging out...")
        self.context.logout()
        self.transition_to(StatesEnum.SPLASH)
