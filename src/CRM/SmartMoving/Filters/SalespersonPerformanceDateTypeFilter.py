
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SalespersonPerformanceDateTypeFilter(OfficeCalendarEventFilter):
    
    def _locate(self):
        return WebDriverWait(self._driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='display-value' and normalize-space(text())='Move Date']")))
         




