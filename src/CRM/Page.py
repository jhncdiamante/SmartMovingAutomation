from abc import ABC, abstractmethod

class Page(ABC):
    
    @property
    @abstractmethod
    def _locator(self):
        """Subclasses must provide their menu XPath"""
        pass

    @abstractmethod
    def open(self) -> None: pass

    @abstractmethod
    def _wait_for_complete_loading(self): pass

