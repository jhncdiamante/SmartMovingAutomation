from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Chrome.IDriver import IDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from src.CRM.SmartMoving.Filters.LostLeadsAndOpportunitiesSummaryDateFilter import LostLeadsAndOpportunitiesSummaryDateFilter




class LostLeadsAndOpportunitiesSummary(InsightsPage):
    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter, date_filter: LostLeadsAndOpportunitiesSummaryDateFilter):
        super().__init__(driver)
        self.calendar_filter = calendar_filter
        self.date_filter = date_filter

    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Lost Leads & Opportunities Summary']")


    def get_price_too_high(self) -> int:
        xpath = "//sm-viper-text-column-template[normalize-space(text())='Price Too High']/parent::td/following-sibling::td[1]"
        price_el = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return price_el.text.strip()