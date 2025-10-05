from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EstimateAccuracySummary(InsightsPage):
    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter):
        super().__init__(driver)
        self.calendar_filter = calendar_filter

    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Estimate Accuracy Summary']")


    def get_average_price(self) -> float:
        average_price_xpath = "//tbody//tr[.//text()[normalize-space()='Erik Cairo']]/td[3]"

        average_price = WebDriverWait(
            self._driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, average_price_xpath))
        )
        return float(average_price.replace("$", "").replace(",", "").strip())

