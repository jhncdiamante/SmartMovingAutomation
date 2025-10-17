
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import DefaultFilter

import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class SalesDashboardSalesPersonFilter(DefaultFilter):
    @property
    def _locator(self):
        return By.XPATH, "//span[@class='display-value']"

    def click(self) -> bool:
        try:
            self._logger.info("Refreshing page before clicking SalesPerson filter...")
            self._driver.refresh()

            # Wait for full page load
            WebDriverWait(self._driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)

            # Now call the original click() from the parent
            return super().click()

        except WebDriverException as e:
            self._driver.save_screenshot("refresh_click_error.png")
            self._logger.error(f"SalesDashboardSalesPersonFilter.click failed: {e}")
            raise
         




