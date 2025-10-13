from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import By
from selenium.webdriver.support import expected_conditions as EC
from abc import abstractmethod
from src.Helpers.logging_config import setup_logger

class ScorecardTable:
    DEFAULT_TIMEOUT = 60
    def __init__(self, driver: WebDriver):
        self._driver = driver
        cls = self.__class__
        self._logger = setup_logger(f"{cls.__module__}.{cls.__name__}")
        self._logger.info(f"Initialized {cls.__name__}")

    @property
    @abstractmethod
    def _locator(self) -> tuple[By, str]: pass

    def set_value(self, title: str, value: str, week: str) -> None:
        """
        Locates the column matching the specified week in a row matching the specified title.
        Finally, fills the located cell with the specified value.
        """
        xpath = f"//div[@row-index and .//text()[normalize-space()='{title}']]//div[@col-id='{week}T00:00:00.000Z']"
        try:
            cell = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except TimeoutException:
            self._logger.warning(f"Failed to locate cell for {title} and {week}.")
            return
        cell.send_keys(value)
        WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
            EC.text_to_be_present_in_element_value((By.XPATH, xpath))
        )

    def open(self):
        """
        Locates and clicks the dropdown, and then selects the table type to open it.
        """
        nav_dropdown = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.TAG_NAME, "ninety-scorecard-team-select"))
        )
        nav_dropdown.click()

        table_name_option = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(self._locator)
        )
        table_name_option.click()
        
