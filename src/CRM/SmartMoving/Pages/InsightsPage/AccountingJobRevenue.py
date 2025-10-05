from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Chrome.IDriver import IDriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.CRM.SmartMoving.Filters.AccountingJobRevenueDateTypeFilter import AccountingJobRevenueDateFilter

from src.Helpers.logging_config import setup_logger

log = setup_logger(__name__)

from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
class AccountingJobRevenue(InsightsPage):
    def __init__(self, driver: IDriver, date_filter: AccountingJobRevenueDateFilter, calendar_filter: CalendarFilter):
        super().__init__(driver)
        self.date_filter = date_filter
        self.calendar_filter = calendar_filter

    @property
    def _locator(self) -> str:
        return (By.XPATH,"//a[normalize-space(text())='Accounting Job Revenue']")


    def get_net_revenue(self) -> float:                  
        xpath = "//td[.//div[normalize-space(text())='Net Revenue (less taxes and tips)']]//following-sibling::td"

        net_revenue_value = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return float(net_revenue_value.text.replace("$", "").replace(",", "").strip())



    def open_modal(self, item: str) -> None:
        item_el_xpath = f"//div[@class='clickable-metric' and normalize-space(text()) = '{item}']"
        WebDriverWait(self._driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, item_el_xpath))
        ).click()


    def close_modal(self) -> None:
        modal_close_button_css_selector = "a.modal-close.icon-close"
        WebDriverWait(self._driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, modal_close_button_css_selector))
        ).click()


    def get_number_of_valuation_closed(self) -> int:
        valuation_closed_els_xpath = "//td[.//sm-viper-text-column-template[normalize-space(text())='Closed']]"
        valuation_closed_els = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_all_elements_located((By.XPATH, valuation_closed_els_xpath))
        )

        return len(valuation_closed_els)

    def get_total_valuation_cost(self) -> float:
        xpath = "//div[@class='modal-body']//table/tbody//tr/td[last()]"

        elements = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath))
        )

        total = 0.0
        for el in elements:
            text = el.text.strip().replace("$", "").replace(",", "")
            if not text:
                continue
            try:
                total += float(text)
            except ValueError:
                continue  

        return total


        




