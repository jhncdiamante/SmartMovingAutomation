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

    def _locate(self):
        return WebDriverWait(self._driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//sm-filter-date//button[contains(normalize-space(.), 'This Month')]")))


    def click(self):
        filter_icon = self._locate()
        filter_icon.click()


    def _click_navigation_button(self, nav: str):
        assert nav == "Past" or nav == "Future"
        self._driver.find_element(
            By.XPATH,
            f"//div[@class='quick-filter-container']/div/sm-button[{1 if nav == 'Past' else 2}]/button"
        ).click()

    def select_value(self, value: str="This Week"):
        value_xpath = f"//button[contains(normalize-space(.), '{value}')]"


        if value in FILTER_OPTIONS["Past"]:
            self._click_navigation_button("Past")
        elif value in FILTER_OPTIONS["Future"]:
            self._click_navigation_button("Future")
        elif value not in FILTER_OPTIONS["Present"]:
            raise ValueError(f"Invalid value for calendar filter: {value}")

        
        filter_container = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.quick-filter-container"))
        )
        value_el = WebDriverWait(filter_container, 60).until(
            EC.element_to_be_clickable((By.XPATH, value_xpath))
        )

        value_el.click()

        button_xpath = "//button[contains(normalize-space(.), 'Apply')]"

        button_el = WebDriverWait(self._driver, 60).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        button_el.click()