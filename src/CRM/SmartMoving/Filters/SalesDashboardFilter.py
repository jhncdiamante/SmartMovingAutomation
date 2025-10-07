
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SalesDashboardSalesPersonFilter(OfficeCalendarEventFilter):
    @property
    def _locate(self):
        return (By.XPATH, "//span[@class='display-value']")
         




