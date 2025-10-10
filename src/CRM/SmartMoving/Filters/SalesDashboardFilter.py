
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter

from selenium.webdriver.common.by import By


class SalesDashboardSalesPersonFilter(OfficeCalendarEventFilter):
    @property
    def _locate(self):
        return By.XPATH, "//span[@class='display-value']"
         




