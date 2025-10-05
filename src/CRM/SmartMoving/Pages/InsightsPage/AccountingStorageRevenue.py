from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from selenium.webdriver.common.by import By
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Filters.QuickDateFilter import QuickDateFilter


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccountingStorageRevenue(InsightsPage):
    def __init__(self, driver: IDriver, quick_date_filter: QuickDateFilter):
        super().__init__(driver)
        self.quick_date_filter = quick_date_filter

    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Accounting Storage Revenue']")

    def get_net_invoiced(self) -> float:
        xpath = "//table/tbody/tr[last()]/th[last()]"

        net_invoiced_value = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return float(net_invoiced_value.replace("$", "").replace(",", "").strip())