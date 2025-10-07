from selenium.common.exceptions import TimeoutException
from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EstimateAccuracySummary(InsightsPage):
    DEFAULT_TIMEOUT = 60

    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter):
        super().__init__(driver)
        self.calendar_filter = calendar_filter

    @property
    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Estimate Accuracy Summary']")


    def get_average_price(self, salesperson: str) -> float | None:
        average_price_xpath = f"//tbody//tr[.//text()[normalize-space()='{salesperson}']]/td[3]"
        self._logger.info(f"Attempting to get the average price for {salesperson}...")

        try:
            average_price = WebDriverWait(
                self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, average_price_xpath))
            )
            self._logger.info(f"Extracted average price: {average_price}")
        except TimeoutException:
            self._logger.warning("Failed to get the average price under 60 seconds.")
            return
        try:
            return float(average_price.text.replace("$", "").replace(",", "").strip())
        except ValueError:
            self._logger.warning(f"Unable to convert {average_price.text} to float.")

