"""
Módulo responsável por criar os elementos do calendário

Classes:
    EventFactory: classe responsável por criar os elementos do calendário
"""
from ..calendar_elements.element_interface import Element

class ElementFactory:
    """
    A Factory class for creating different types of calendar elements.
    """

    @staticmethod
    def create_element(element_type: str,
                        element_id: str,
                        title: str,
                        schedules: [str],
                       **kwargs) -> Element:
        """
        Create a calendar element based on the provided type.

        Arguments:
            element_type -- The type of the calendar element to create.
            element_id -- The id of the element.
            title -- The title of the element.
            schedules -- The schedules that the element belongs to.
            **kwargs -- Additional arguments specific to each element type.

        Returns:
            Element -- An instance of the specified calendar element type.
        """
        from ..calendar_elements.element_types import EventElement,\
                                                        TaskElement,\
                                                        ReminderElement
        if element_type == "event":
            return EventElement(element_id,
                                title,
                                kwargs['start'],
                                kwargs['end'],
                                schedules,
                                kwargs['description'])
        elif element_type == "task":
            return TaskElement(element_id,
                                title,
                                kwargs['due_date'],
                                schedules,
                                kwargs['description'])
        elif element_type == "reminder":
            return ReminderElement(element_id,
                                    title,
                                    kwargs['reminder_date'],
                                    schedules,
                                    kwargs['description'])
        else:
            raise ValueError(f"Unsupported element type: {element_type}")
