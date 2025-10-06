from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.CRM.SmartMoving.Filters.SalespersonPerformanceDateTypeFilter import SalespersonPerformanceDateTypeFilter
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from selenium.common.exceptions import TimeoutException

class SalespersonPerformance(InsightsPage):
    def __init__(self, calendar_filter: CalendarFilter, date_type_filter: SalespersonPerformanceDateTypeFilter):
        self.calendar_filter = calendar_filter
        self.date_type_filter = date_type_filter

    def get_bad_leads(self) -> int | None:
        xpath = "//span[normalize-space(text())='Bad']/following-sibling::h2/span[1]"
        self._logger.info("Attempting to get bad leads count...")
        try:
            bad_leads_el = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return int(bad_leads_el.text.strip())
        except TimeoutException:
            self._logger.warning("Failed to get bad leads count under 60 seconds.")
        except ValueError:
            self._logger.warning(f"Unable to convert {bad_leads_el.text} to int.")


    def get_bad_leads_percentage(self) -> str | None:
        xpath = "//span[normalize-space(text())='Bad']/following-sibling::h2/span[2]"

        self._logger.info("Attempting to get bad leads percentage...")
        try:
            bad_leads_percentage_el = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return bad_leads_percentage_el.text.strip()
        except TimeoutException:
            self._logger.warning("Failed to get bad leads percentage under 60 seconds.")
        except ValueError:
            self._logger.warning(f"Unable to convert {bad_leads_percentage_el.text} to int.")


        