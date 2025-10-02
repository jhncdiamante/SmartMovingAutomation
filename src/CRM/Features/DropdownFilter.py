from abc import abstractmethod, ABC

from src.Chrome.IDriver import IDriver

class DropdownFilter(ABC):
    def __init__(self, driver: IDriver):
        self._driver = driver

    @abstractmethod
    def click(self):
        '''
        This method will locate the filter icon using identifier (e.g. XPATH, ID, CSS_SELECTOR), and clicks it using Selenium.
        The method will also wait for the visibility of the popup window or the options that shall appear after clicking the filter icon.
        '''
        pass

    @property
    @abstractmethod
    def options(self):
        '''
        This method will return the filter options present in the dropdown
        '''
        pass      

    @abstractmethod
    def select_value(self):
        '''
        This method will select a value in the dropdown
        '''
        pass






