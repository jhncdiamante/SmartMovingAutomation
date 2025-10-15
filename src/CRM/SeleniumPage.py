from src.CRM.Page import Page
from src.Drivers.IDriver import IDriver
from src.Helpers.logging_config import setup_logger
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import By

class SeleniumPage(Page):
    
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
        raise NotImplementedError

    def open(self) -> None:
        self._logger.info("Opening page...")
        element = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self._locator)
            )
        element.click()
        time.sleep(5)