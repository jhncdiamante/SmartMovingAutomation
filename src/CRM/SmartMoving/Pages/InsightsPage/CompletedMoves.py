
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)
from undetected_chromedriver import WebElement

from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Drivers.IDriver import IDriver

from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter

import time

class CompletedMoves(InsightsPage):
    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter):
        super().__init__(driver)
        self.calendar_filter = calendar_filter

    @property
    def _locator(self) -> tuple[By, str]:
        return (By.XPATH, "//a[normalize-space(text())='Completed Moves']")

    def _get_next_button(self) -> WebElement | None:
        next_button_xpath = "//li[a[normalize-space(text())='Next']]"
        try:
            return WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, next_button_xpath))
            )
        except TimeoutException:
            self._logger.info("Pagination Next button not found; likely single page of results.")
        except WebDriverException as e:
            self._logger.warning(f"Failed to get next button due to error: {e}")


    def get_total_moves(self) -> int | None:
        rows_xpath = "//table/tbody/tr/td[11]"
        no_data_xpath = "//td[normalize-space(text())='No data matches your current filters. Please adjust and try again.']"
        count = 0
        try:
            WebDriverWait(self._driver, 5).until(
                            EC.visibility_of_element_located((By.XPATH, no_data_xpath))
                        )
            self._logger.info("No booked opportunities found (empty dataset).")
            return 0
        except TimeoutException:

            while True:
                try:
                    rows = WebDriverWait(self._driver, 15).until(
                        EC.visibility_of_all_elements_located((By.XPATH, rows_xpath))
                    ) 
                    rows = [row for row in rows if row.text.strip() and float(row.text.replace("$", "").replace(",", "").strip()) > 0]
                    page_count = len(rows)
                    if page_count > 0:
                        count += page_count
                    self._logger.info(f"Found {page_count} moves (Total so far: {count}).")

                    next_button_li = self._get_next_button()
                    if not next_button_li:
                        break

                    li_class = next_button_li.get_attribute("class") or ""
                    if "disabled" in li_class:
                        self._logger.info("Reached last page; pagination complete.")
                        break

                    next_button_li.click()
                    time.sleep(5)

                except Exception as e:
                    self._logger.warning(f"Unexpected error while counting rows: {e}")
                    return None

            self._logger.info(f"Final total moves: {count}")
            return count