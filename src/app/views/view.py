from __future__ import annotations
from abc import ABC, abstractmethod


class View(ABC):
    """
    The View's interface is responsible for rendering the UI.
    It is supposed to be inside a root element, and renders elements there.

    args:
        root: the root element of the UI.

    attributes:
        root: the root element of the UI.
    
    methods:
        show: renders the UI.
    """

    def __init__(self, root) -> None:
        """
        The View's interface is responsible for rendering the UI.
        It is supposed to be inside a root element, and renders elements there.

        args:
            root: the root element of the UI.

        attributes:
            root: the root element of the UI.
        """
        self.root = root

    @abstractmethod
    def show(self) -> None:
        """
        The View's interface is responsible for rendering the UI.
        """

    def clear_view(self) -> None:
        """
        Clears the view.
        """
        for child in self.root.winfo_children():
            child.destroy()