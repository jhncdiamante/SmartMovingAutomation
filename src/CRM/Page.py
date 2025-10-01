from abc import ABC, abstractmethod

class IPage(ABC):
    @abstractmethod
    def open(self): pass
