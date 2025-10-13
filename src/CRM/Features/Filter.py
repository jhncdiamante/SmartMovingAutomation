from abc import abstractmethod, ABC

from src.SeleniumDriver.IDriver import IDriver
from src.Helpers.logging_config import setup_logger

from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import WebElement

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Filter(ABC):
    DEFAULT_TIMEOUT = 60
    def __init__(self, driver: IDriver):
        self._driver = driver
        cls = self.__class__
        self._logger = setup_logger(f"{cls.__module__}.{cls.__name__}")
        self._logger.info(f"Initialized {cls.__name__}")

    @abstractmethod
    def click(self):
        pass

    @abstractmethod
    def select_value(self):
        '''
        This method will select a value in the dropdown
        '''
        pass

    def _locate(self) -> WebElement | None:
        try:
            self._logger.info("Locating filter button...")
            return WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(EC.element_to_be_clickable(self._locator))
        except TimeoutException:
            self._logger.error("Failed to locate filter button.")


    @property
    @abstractmethod
    def _locator(self): pass






