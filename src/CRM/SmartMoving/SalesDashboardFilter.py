
from src.CRM.SmartMoving.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SalesDashboardSalesPersonFilter(OfficeCalendarEventFilter):
    def _locate_dropdown(self):
        return WebDriverWait(self._driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='display-value']")))
         




