from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from src.CRM.Features.Filter import Filter
import time
class SidePanelFilter(Filter):
    def _wait_for_clickable(self, xpath: str, timeout: int = 60) -> WebElement:
        return WebDriverWait(self._driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

    def _locate(self) -> WebElement:
        return self._wait_for_clickable("//button[normalize-space(.)='Filters']")

    def click(self) -> None:
        self._locate().click()

    def select_value(self, filter_type: str, selected_values: list) -> None:
        filter_type_xpath = f"//sm-viper-filter-list-slideout//sm-filter-list//sm-button//button//div/div[normalize-space(text())='{filter_type}']"
        self._wait_for_clickable(filter_type_xpath).click()

        for val in selected_values:
            value_xpath = f"//label[normalize-space(text())='{val}']"
            option = self._wait_for_clickable(value_xpath)
            option.click()
            time.sleep(1)

    def apply(self) -> None:
        apply_xpath = "//button[normalize-space(.)='Apply']"
        self._wait_for_clickable(apply_xpath).click()
        # Wait for panel to close (if applicable)
        WebDriverWait(self._driver, 60).until_not(
            EC.presence_of_element_located((By.XPATH, apply_xpath))
        )

    def close(self) -> None:
        close_xpath = "//span[@data-test-id='close-panel']"
        self._wait_for_clickable(close_xpath).click()
        WebDriverWait(self._driver, 60).until_not(
            EC.presence_of_element_located((By.XPATH, close_xpath))
        )
