from abc import abstractmethod, ABC

from src.Chrome.IDriver import IDriver

class Filter(ABC):
    def __init__(self, driver: IDriver):
        self._driver = driver

    @abstractmethod
    def click(self):
        pass

    @abstractmethod
    def select_value(self):
        '''
        This method will select a value in the dropdown
        '''
        pass

    @abstractmethod
    def _locate(self):
        '''
        This method will locate the filter icon using identifier (e.g. XPATH, ID, CSS_SELECTOR)
        '''
        pass






