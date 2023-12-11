"""
Module that contains the observer interface.
"""
from abc import ABC, abstractmethod

class Subject(ABC): ...

class Observer(ABC):
    """
    Observer interface, used to implement the observer pattern.
    Solve the problem of circular dependencies between the instance and 
    their manager.
    Provide a update method that is called when the instance is updated.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Called when the schedule is updated.

        Arguments:
            schedule -- the schedule that was updated.
        """
        pass

class Subject(ABC):
    """
    Subject interface, used to implement the observer pattern in the schedule.
    solve the problem of circular dependencies between the schedule and the 
    schedule management.
    provide a attach method that is called when the schedule is updated.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.

        Arguments:
            observer -- the observer to attach.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.

        Arguments:
            observer -- the observer to detach.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all the observers that the subject has changed.
        """
        pass
