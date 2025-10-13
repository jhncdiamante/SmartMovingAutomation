from src.CRM.Page import Page
from src.SeleniumDriverumDriverumDriverumDriver.IDriver import IDriver
from src.Helpers.logging_config import setup_logger

class SmartMovingPage(Page):
    DEFAULT_TIMEOUT = 60
    def __init__(self, route: str, driver: IDriver):
        self._route = route
        self._driver = driver
        cls = self.__class__
        self._logger = setup_logger(f"{cls.__module__}.{cls.__name__}")
        self._logger.info(f"Initialized {cls.__name__}")


    
        
    def open(self):
        self._driver.get(self._route)
        self._wait_for_complete_loading()

    