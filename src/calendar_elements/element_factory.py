"""
Módulo responsável por criar os elementos do calendário

Classes:
    EventFactory: classe responsável por criar os elementos do calendário
"""
from ..calendar_elements.element_types import EventElement, TaskElement, ReminderElement
from ..calendar_elements.element_interface import Element


class ElementFactory:
    """
    A Factory class for creating different types of calendar elements.
    """

    @staticmethod
    def create_element(element_type: str, element_id: str, title: str, **kwargs) -> Element:
        """
        Create a calendar element based on the provided type.

        Arguments:
            element_type -- The type of the calendar element to create.
            element_id -- The id of the element.
            title -- The title of the element.
            **kwargs -- Additional arguments specific to each element type.

        Returns:
            Element -- An instance of the specified calendar element type.
        """
        if element_type == "evento":
            return EventElement(element_id, title, kwargs['start'], kwargs['end'])
        elif element_type == "tarefa":
            return TaskElement(element_id, title, kwargs['description'], kwargs['due_date'])
        elif element_type == "lembrete":
            return ReminderElement(element_id, title, kwargs['description'],
                                   kwargs['reminder_date'])
        else:
            raise ValueError(f"Unsupported element type: {element_type}")
