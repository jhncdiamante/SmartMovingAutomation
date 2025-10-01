
from src.CRM.SmartMoving.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SalesDashboardSalesPersonFilter(OfficeCalendarEventFilter):
    def click(self):
        dropdown = WebDriverWait(self._driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='display-value']")))
        dropdown.click()
        WebDriverWait(self._driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ngb-popover-window.popover.show")))


