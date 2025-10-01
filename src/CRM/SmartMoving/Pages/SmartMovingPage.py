from selenium.webdriver.support.ui import WebDriverWait
from src.CRM.Page import IPage
from src.Chrome.IDriver import IDriver

class SmartMovingPage(IPage):
    def __init__(self, route: str, driver: IDriver):
        self._route = route
        self._driver = driver

    def _wait_for_complete_loading(self, timeout=30):
        WebDriverWait(self._driver, timeout).until(
            lambda _: self._driver.execute_script("return document.readyState")
            == "complete"
        )
        
    def open(self):
        self._driver.get(self._route)
        self._wait_for_complete_loading()

    