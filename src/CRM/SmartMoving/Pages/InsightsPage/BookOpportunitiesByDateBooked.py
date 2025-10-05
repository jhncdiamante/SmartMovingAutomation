from selenium.webdriver.ie.webdriver import WebDriver
from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.CRM.SmartMoving.Filters.SidePanelFilter import SidePanelFilter
from selenium.common.exceptions import TimeoutException

class BookedOpportunitiesByDateBooked(InsightsPage):
    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter, side_panel_filter: SidePanelFilter):
        super().__init__(driver)
        self.calendar_filter = calendar_filter
        self.side_panel_filter = side_panel_filter

    @property
    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Booked Opportunities by Date Booked']")

    def get_total_estimated_amount(self) -> float or str:
        xpath = "//span[normalize-space(text())='Estimated Amount']//following-sibling::h2/span[1]"

        total_estimated_amount = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        try:
            return float(total_estimated_amount.text.replace("$", "").replace(",", "").strip())
        except ValueError:
            return 0.0 if total_estimated_amount.text.strip() == "--" else "ERROR"
            

            
    def get_total_booked_count(self) -> int or str:
        rows_with_booked_status_xpath = "//td[.//text()[normalize-space()='Booked']]"
        try:
            rows_with_booked_status = WebDriverWait(self._driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, rows_with_booked_status_xpath))
            )
        except TimeoutException:
            try:
                WebDriverWait(self._driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//td[.//text()[normalize-space()='No data matches your current filters. Please adjust and try again.']]")))
                return 0
            except TimeoutException:
                return "ERROR"
        return len(rows_with_booked_status)
        