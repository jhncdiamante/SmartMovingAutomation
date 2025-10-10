
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter

from selenium.webdriver.common.by import By

class SalespersonPerformanceDateTypeFilter(OfficeCalendarEventFilter):
    @property
    def _locator(self):
        return By.XPATH, "//span[@class='display-value' and normalize-space(text())='Move Date']"
         




