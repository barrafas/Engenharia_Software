from abc import ABC, abstractmethod

class State(ABC):
    """
    The base State class declares methods that all Concrete State should
    implement and also provides a backreference to the Application object,
    associated with the State. This backreference can be used by States to
    transition the Application to another State.
    """

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
    def logout(self) -> None:
        """
        Handle logout request.
        """

    @abstractmethod
    def go_back(self) -> None:
        """
        Handle go back request.
        """

    @abstractmethod
    def render(self) -> None:
        """
        Handle render request.
        """

    def clear(self) -> None:
        """
        Handle clear request.
        """
