from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import By
from selenium.webdriver.support import expected_conditions as EC
from abc import abstractmethod

class ScorecardTable:
    TIMEOUT = 60
    def __init__(self, driver: WebDriver):
        self._driver = driver

    @property
    @abstractmethod
    def _locator(self) -> tuple[By, str]: pass

    def set_value(self, title: str, value: str, week: str) -> None:
        xpath = f"//div[@row-index and .//text()[normalize-space()='{title}']]//div[@col-id='{week}T00:00:00.000Z']"
        cell = WebDriverWait(self._driver, self.TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        print(f"Title: {cell.text.strip()}")
        #cell.send_keys(value)

    def open(self):
        nav_dropdown = WebDriverWait(self._driver, self.TIMEOUT).until(
            EC.element_to_be_clickable((By.TAG_NAME, "ninety-scorecard-team-select"))
        )
        nav_dropdown.click()

        table_name_option = WebDriverWait(self._driver, self.TIMEOUT).until(
            EC.element_to_be_clickable(self._locator)
        )
        table_name_option.click()
        
