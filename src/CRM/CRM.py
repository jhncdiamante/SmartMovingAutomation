
from abc import ABC, abstractmethod
from src.Login.LoginCredentials import LoginCredentials
from selenium.webdriver.support.ui import WebDriverWait

class CustomerRelationshipManagementSoftware(ABC):
    def __init__(self, base_url: str, login_credentials: LoginCredentials, selenium_driver):
        self.base_url = base_url
        self._login_credentials = login_credentials
        self._selenium_driver = selenium_driver
        self._driver = self._selenium_driver.driver

    def open(self):
        self._driver.get(self.base_url)
        self._wait_for_complete_loading()


    def _wait_for_complete_loading(self, timeout=30):
        WebDriverWait(self._driver, timeout).until(
            lambda _: self._driver.execute_script("return document.readyState")
            == "complete"
        )

    @abstractmethod
    def close(self): pass

    @abstractmethod
    def login(self): pass
