from src.CRM.Page import Page
from src.Chrome.IDriver import IDriver

class SmartMovingPage(Page):
    def __init__(self, route: str, driver: IDriver):
        self._route = route
        self._driver = driver

    
        
    def open(self):
        self._driver.get(self._route)
        self._wait_for_complete_loading()

    