from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from src.Helpers.logging_config import setup_logger
from src.SeleniumDriver.IDriver import IDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.Helpers.logging_config import setup_logger
import time
class Page(ABC):
    
    DEFAULT_TIMEOUT = 60
    def __init__(self, driver: IDriver):
        self._driver = driver
        cls = self.__class__
        self._logger = setup_logger(f"{cls.__module__}.{cls.__name__}")
        self._logger.info(f"Initialized {cls.__name__}")

    
    def _wait_for_complete_loading(self, timeout=60):
        WebDriverWait(self._driver, timeout).until(
            lambda _: self._driver.execute_script("return document.readyState")
            == "complete"
        )
    @property
    def _locator(self) -> tuple[By, str]:
        """Subclasses must provide their menu XPath"""
        pass

    def open(self) -> None:
        self._logger.info("Opening page...")
        element = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self._locator)
            )
        element.click()
        time.sleep(5)