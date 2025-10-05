from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait


class Page(ABC):
    @abstractmethod
    def open(self): pass

    def _wait_for_complete_loading(self, timeout=60):
        WebDriverWait(self._driver, timeout).until(
            lambda _: self._driver.execute_script("return document.readyState")
            == "complete"
        )
