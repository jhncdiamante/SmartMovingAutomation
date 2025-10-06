from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from selenium.webdriver.common.by import By
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Filters.QuickDateFilter import QuickDateFilter

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class AccountingStorageRevenue(InsightsPage):
    DEFAULT_TIMEOUT = 60

    def __init__(self, driver: IDriver, quick_date_filter: QuickDateFilter):
        super().__init__(driver)
        self.quick_date_filter = quick_date_filter

    @property
    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Accounting Storage Revenue']")

    def get_net_invoiced(self) -> float:
        xpath = "//table/tbody/tr[last()]/th[last()]"

        try:
            net_invoiced_value = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )  
        except TimeoutException:
            self._logger.warning("Failed to get net invoiced under 60 seconds.")
            return None
        except WebDriverException as e:
            self._logger.warning(f"Failed to get net invoiced due to error: {e}")
        self._logger.info(f"Extracted net invoiced value raw text: {net_invoiced_value.text}")
        try:
            return float(net_invoiced_value.text.replace("$", "").replace(",", "").strip())
        except ValueError:
            self._logger.warning(f"Unable to convert raw text {net_invoiced_value.text} to float.")