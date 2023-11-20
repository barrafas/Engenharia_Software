from abc import ABC, abstractmethod
from datetime import datetime

class Event(ABC):
    @abstractmethod
    def display_info(self):
        pass
