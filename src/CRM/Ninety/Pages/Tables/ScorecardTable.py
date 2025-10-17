from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import By
from selenium.webdriver.support import expected_conditions as EC
from abc import abstractmethod
from src.Helpers.logging_config import setup_logger
from selenium.webdriver.common.keys import Keys
import time
# src/CRM/Ninety/Pages/Tables/ScorecardTable.py
from abc import abstractmethod
from playwright.sync_api import Page as PlaywrightPage
from src.Helpers.logging_config import setup_logger


class ScorecardTable:
    DEFAULT_TIMEOUT = 120_000  # milliseconds

    def __init__(self, page: PlaywrightPage):
        self._page = page
        cls = self.__class__
        self._logger = setup_logger(f"{cls.__module__}.{cls.__name__}")
        self._logger.info(f"Initialized {cls.__name__}")

    @property
    @abstractmethod
    def _locator(self) -> str:
        """Each subclass defines its table name locator"""
        pass

    def set_value(self, title: str, value: str, week: str) -> None:
        """
        Locates the column matching the specified week in a row matching the specified title.
        Then focuses the cell, types the value, and commits it (AG-Grid style).
        """
        xpath = (
            f"//div[@row-index and .//text()[normalize-space()='{title}']]"
            f"//div[@col-id='{week}T00:00:00.000Z']"
        )

        try:
            cell = self._page.locator(xpath)
            cell.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)

            # Ensure focus
            cell.click(timeout=self.DEFAULT_TIMEOUT)
            self._page.wait_for_timeout(300)  # brief delay for focus

            self._page.keyboard.type(str(value))
            self._page.keyboard.press("Enter")

            self._logger.info(f"Value set for '{title}' at '{week}': {value}")

        except Exception as e:
            self._logger.warning(f"Failed to locate or set value for {title} ({week}): {e}")


    def open(self):
        """Locates and clicks the dropdown, then selects this table type."""
        self._logger.info(f"Opening {self}...")
        nav_dropdown = self._page.locator("ninety-scorecard-team-select")
        nav_dropdown.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        nav_dropdown.click()

        table_option = self._page.locator(self._locator)
        table_option.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        table_option.click()

        self._page.wait_for_timeout(10_000)
