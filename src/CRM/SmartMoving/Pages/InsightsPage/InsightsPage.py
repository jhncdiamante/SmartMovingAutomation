from src.CRM.Page import Page
from src.Chrome.IDriver import IDriver
from abc import abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InsightsPage(Page):
    def __init__(self, driver: IDriver):
        self._driver = driver

    @property
    @abstractmethod
    def _locator(self) -> tuple[By, str]:
        """Subclasses must provide their menu XPath"""
        pass

    def open(self) -> None:
        element = WebDriverWait(self._driver, 60).until(
            EC.element_to_be_clickable(self._locator)
        )
        element.click()

    def close(self):
        self._driver.get("https://app.smartmoving.com/reports/smart-insights/lists")
        self._wait_for_complete_loading()