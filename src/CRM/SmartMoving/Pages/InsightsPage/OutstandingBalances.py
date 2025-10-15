
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.Drivers.IDriver import IDriver
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
class OutstandingBalances(InsightsPage):
    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter):
        super().__init__(driver)
        self.calendar_filter = calendar_filter

    @property
    def _locator(self) -> tuple[By, str]:
        return By.XPATH,"//a[normalize-space(text())='Outstanding Balances']"

    
    def get_total_balance(self) -> float | None:
        xpath = "//table/tbody/tr/td[last()]"
        self._logger.info("Attempting to get total balance...")
        try:
            balances = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath))
            )
        except TimeoutException:
            self._logger.warning(f"Failed to get total balance under {self.DEFAULT_TIMEOUT} seconds")
            return 

        try:    
            return sum([float(balance.text.replace("$", "").replace(",", "").strip()) for balance in balances if balance.text.strip()])
        except ValueError:
            self._logger.warning(f"Unable to sum all balances: {balances.text}.")
            
    