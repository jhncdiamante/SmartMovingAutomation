from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from src.CRM.Features.Filter import Filter
import time

class SidePanelFilter(Filter):
    def _wait_for_clickable(self, xpath: str, timeout: int = 60) -> WebElement | None:
        try:
            return WebDriverWait(self._driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except TimeoutException:
            pass

    @property
    def _locator(self) -> tuple[By, str]:
        return By.XPATH, "//button[normalize-space(.)='Filters']"

    def click(self) -> bool:
        filter_button = self._locate()
        if not filter_button:
            self._logger.error("No filter button found. Unable to click button.")
            return False
        try:
            filter_button.click()
            return True
        except WebDriverException as e:
            self._logger.error(f"Failed to click side panel filter due to error: {e}")

    def select_value(self, filter_type: str, selected_values: list) -> bool:
        filter_type_xpath = f"//sm-viper-filter-list-slideout//sm-filter-list//sm-button//button//div/div[normalize-space(text())='{filter_type}']"
        filter_type = self._wait_for_clickable(filter_type_xpath)
        if not filter_type:
            self._logger.error(f"Failed to locate filter type {filter_type} to be clicked.")
            raise Exception


        self._logger.info("Attempting to click filter type button...")
        try:
            filter_type.click()
        except WebDriverException:
            self._logger.error(f"Failed to click filter type {filter_type}.")
            raise Exception

        self._logger.info("Attempting to click selected values...")
        for val in selected_values:
            value_xpath = f"//label[normalize-space(text())='{val}']"
            option = self._wait_for_clickable(value_xpath)
            if not option:
                self._logger.error(f"Failed to locate {val} option.")
                raise Exception
                
            try:
                option.click()
            except WebDriverException as e:
                self._logger.error(f"Failed to click option {val}.")
                raise Exception
                
            time.sleep(1)
        return True

    def apply(self) -> bool:
        apply_xpath = "//button[normalize-space(.)='Apply']"
        apply_button = self._wait_for_clickable(apply_xpath)
        if not apply_button:
            self._logger.error("Failed to click Apply button.")
            raise Exception
            

        try:
            apply_button.click()
            WebDriverWait(self._driver, 60).until_not(
                EC.presence_of_element_located((By.XPATH, apply_xpath))
            )
            return True
        except TimeoutException:
            self._logger.error("Failed to wait for filter panel to be closed.")
        except WebDriverException as e:
            self._logger.error(f"Failed to click Apply Button due to error: {e}")
        raise Exception


    def close(self) -> bool:
        close_xpath = "//span[@data-test-id='close-panel']"
        close_button = self._wait_for_clickable(close_xpath)
        if not close_button:
            self._logger.error("Failed to close filter panel.")
            raise Exception
            

        try:
            close_button.click()
            WebDriverWait(self._driver, 60).until_not(
                EC.presence_of_element_located((By.XPATH, close_xpath))
            )
            return True
        except TimeoutException:
            self._logger.error("Failed to wait for panel to close.")
        except WebDriverException as e:
            self._logger.error(f"Failed to close due to error: {e}")
