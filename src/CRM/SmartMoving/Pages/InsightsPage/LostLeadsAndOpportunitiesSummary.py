from selenium.common.exceptions import TimeoutException
from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Chrome.IDriver import IDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from src.CRM.SmartMoving.Filters.LostLeadsAndOpportunitiesSummaryDateFilter import LostLeadsAndOpportunitiesSummaryDateFilter




class LostLeadsAndOpportunitiesSummary(InsightsPage):
    DEFAULT_TIMEOUT = 60
    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter, date_filter: LostLeadsAndOpportunitiesSummaryDateFilter):
        super().__init__(driver)
        self.calendar_filter = calendar_filter
        self.date_filter = date_filter

    @property
    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Lost Leads & Opportunities Summary']")


    def get_price_too_high(self) -> int:
        xpath = "//td[.//text()[normalize-space()='Price Too High']]/following-sibling::td[1]"
        price_el = None
        try:
            self._logger.info("Attempting to get price too high...")
            price_el = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return int(price_el.text.strip())
        except TimeoutException:
            self._logger.warning("Failed to get price too high under 60 seconds.")
        except ValueError:
            self._logger.warning(f"Unable to convert {price_el.text} to float.")