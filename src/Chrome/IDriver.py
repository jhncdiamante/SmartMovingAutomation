from abc import ABC, abstractmethod


class IDriver(ABC):
    @abstractmethod
    def _set_up_options(self):
        pass

    @abstractmethod
    def set_up_driver(self):
        pass