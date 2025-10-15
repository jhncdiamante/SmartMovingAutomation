from selenium.common.exceptions import TimeoutException, WebDriverException
from src.CRM.Features.Filter import Filter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class OfficeCalendarEventFilter(Filter):

    def click(self) -> bool:
        self._logger.info("Attempting to click filter button...")
        dropdown = self._locate()
        if not dropdown:
            return False

        try:
            dropdown.click()
            WebDriverWait(self._driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ngb-popover-window.popover.show")))   
            self._logger.info("Successfully clicked filter button.")
            time.sleep(5)
            return True
        except TimeoutException:
            self._logger.error("Failed to wait for visibility of filter popup panel for options.")
        except WebDriverException as e:
            self._logger.error(f"Failed to click filter button due to error: {e}")



    def select_value(self, target: str) -> bool:
        self._logger.info(f"Selecting value {target}...")
        target_xpath = f"//div[@class='label mr-auto' and normalize-space(text())='{target}']"
        try:
            target_el = WebDriverWait(self._driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, target_xpath))
            )
            target_el.click()
            time.sleep(10)
            return True
        except TimeoutException:
            self._logger.error(f"Failed to wait for value {target} to be clicked.")
        except WebDriverException as e:
            self._logger.error(f"Failed to select value {target} due to error: {e}")

    @property
    def _locator(self):
        return (By.XPATH, "//span[@class='display-value' and normalize-space(text())='Any Type']")

 
class OfficeCalendarUserFilter(OfficeCalendarEventFilter):
    @property
    def _locator(self):
        return (By.XPATH, "//span[@class='display-value' and normalize-space(text())='Any User']")





