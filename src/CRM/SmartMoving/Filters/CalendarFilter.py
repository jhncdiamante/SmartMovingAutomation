from typing_extensions import Tuple
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.CRM.Features.Filter import Filter


FILTER_OPTIONS = {
    "Past": {"Yesterday",
             "Last Week",
             "Last Month",
             "Last Quarter",
             "Last Year",
             "Last 90 days",
    },

    "Present": {
             "Today",
             "This Week",
             "This Month",
             "This Quarter",
             "This Year",
             "All Time",
    },

    "Future": {
             "Tomorrow",
             "Next Week",
             "Next Month",
             "Next Quarter",
             "Next Year",
    }
}



class CalendarFilter(Filter):

    @property
    def _locator(self) -> Tuple[By, str]:
        return (By.XPATH, "//sm-button[@materialicon='calendar_today']")


    def click(self):
        filter_icon = self._locate()
        filter_icon.click()


    def _click_navigation_button(self, nav: str) -> bool:

        current_nav = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='quick-filter-container']//span[contains(text(), 'Current') or contains(text(), 'Past') or contains(text(), 'Future') ]"))
        ).text.strip()

        if current_nav == nav:
            return

        assert current_nav == "Current"


        try:
            self._logger.info(f"Locating navigation button {nav}...")
            nav_button = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@class='quick-filter-container']/div/sm-button[{1 if nav == 'Past' else 2}]/button"))
            )
            self._logger.info(f"Clicking navigation button...")
            nav_button.click()
            return True
        except TimeoutException:
            self._logger.error(f"Failed to locate navigation button for {nav}.")
        except WebDriverException as e:
            self._logger.error(f"Failed to click navigation button: {e}")


    def select_value(self, value: str="This Week") -> bool:
        value_xpath = f"//button[contains(normalize-space(.), '{value}')]"

        if value in FILTER_OPTIONS["Past"]:
            self._click_navigation_button("Past")
        elif value in FILTER_OPTIONS["Future"]:
            self._click_navigation_button("Future")
        elif value not in FILTER_OPTIONS["Present"]:
            raise ValueError(f"Invalid value for calendar filter: {value}")

        try:
            filter_container = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.quick-filter-container"))
            )
            value_el = WebDriverWait(filter_container, self.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, value_xpath))
            )

            value_el.click()
            
            button_xpath = "//button[contains(normalize-space(.), 'Apply')]"

            button_el = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            button_el.click()
            return True
        except TimeoutException:
            self._logger.warning("Failed to locate filter container or value element or apply button.")
        except WebDriverException:
            self._logger.warning(f"Failed to select given value due to error: {value}.")

        
