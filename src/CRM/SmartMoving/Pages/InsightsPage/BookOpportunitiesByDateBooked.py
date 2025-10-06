from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
    NoSuchElementException,
)
from undetected_chromedriver import WebElement

from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from src.CRM.SmartMoving.Filters.SidePanelFilter import SidePanelFilter
import time


class BookedOpportunitiesByDateBooked(InsightsPage):
    """Handles interactions and data extraction for the 'Booked Opportunities by Date Booked' insights page."""

    DEFAULT_TIMEOUT = 60

    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter, side_panel_filter: SidePanelFilter):
        if not driver:
            raise ValueError("Driver cannot be None.")
        if not calendar_filter or not side_panel_filter:
            raise ValueError("CalendarFilter and SidePanelFilter instances are required.")

        super().__init__(driver)
        self.calendar_filter = calendar_filter
        self.side_panel_filter = side_panel_filter

    @property
    def _locator(self) -> tuple[By, str]:
        """Locator for the 'Booked Opportunities by Date Booked' section"""
        return (By.XPATH, "//a[normalize-space(text())='Booked Opportunities by Date Booked']")


    def _safe_wait(self, locator: tuple, condition, timeout: int | None = None):
        timeout = timeout or self.DEFAULT_TIMEOUT
        try:
            return WebDriverWait(self._driver, timeout).until(condition(locator))
        except TimeoutException:
            self._logger.warning(f"Timeout waiting for element: {locator}")
        except WebDriverException as e:
            self._logger.warning(f"WebDriver exception while waiting for {locator}: {e}")
        return None

    def _get_next_button(self) -> WebElement | None:
        """Safely retrieves the Next pagination button."""
        next_button_xpath = "//li[a[normalize-space(text())='Next']]"
        try:
            return WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, next_button_xpath))
            )
        except TimeoutException:
            self._logger.info("Pagination Next button not found; likely single page of results.")
        except WebDriverException as e:
            self._logger.warning(f"Failed to get next button due to error: {e}")


    def get_total_estimated_amount(self) -> float | None:
        """Extracts the total estimated amount from the page."""
        xpath = "//span[normalize-space(text())='Estimated Amount']//following-sibling::h2/span[1]"
        self._logger.info("Locating 'Estimated Amount' element...")

        element = self._safe_wait((By.XPATH, xpath), EC.visibility_of_element_located)
        if not element:
            self._logger.warning("Failed to locate Estimated Amount element.")
            return None

        raw_text = (element.text or "").strip()
        if not raw_text or raw_text == "--":
            self._logger.warning(f"No estimated amount available: {raw_text} -> (value is '--' or empty).")
            return 0.0

        try:
            value = float(raw_text.replace("$", "").replace(",", ""))
            self._logger.info(f"Extracted total estimated amount: {value}")
            return value
        except ValueError:
            self._logger.warning(f"Invalid Estimated Amount format: '{raw_text}'")
        except Exception as e:
            self._logger.warning(f"Unexpected error parsing Estimated Amount: {e}")

    def get_total_booked_count(self) -> int | None:
        """
        Counts the number of booked opportunities across paginated tables.
        Handles dynamic re-rendering and stale elements gracefully.
        """
        booked_xpath = "//td[.//text()[normalize-space(.)='Booked']]"
        no_data_xpath = "//td[normalize-space(text())='No data matches your current filters. Please adjust and try again.']"
        count = 0

        self._logger.info("Starting booked opportunities count...")

        while True:
            try:
                booked_rows = WebDriverWait(self._driver, 15).until(
                    EC.visibility_of_all_elements_located((By.XPATH, booked_xpath))
                )
                page_count = len(booked_rows)
                count += page_count
                self._logger.info(f"Found {page_count} booked opportunities (Total so far: {count}).")

                # Try to get the pagination next button fresh each iteration
                next_button_li = self._get_next_button()
                if not next_button_li:
                    break

                li_class = next_button_li.get_attribute("class") or ""
                if "disabled" in li_class:
                    self._logger.info("Reached last page; pagination complete.")
                    break
                
                next_button_li.click()
                time.sleep(5)

            except TimeoutException:
                try:
                    WebDriverWait(self._driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, no_data_xpath))
                    )
                    self._logger.info("No booked opportunities found (empty dataset).")
                    return 0
                except TimeoutException:
                    self._logger.warning("Timeout while waiting for booked rows or 'no data' message.")
                    return None
            except (StaleElementReferenceException, NoSuchElementException):
                self._logger.warning("DOM updated or pagination element missing; ending pagination.")
                break
            except Exception as e:
                self._logger.warning(f"Unexpected error while counting booked opportunities: {e}")
                break

        self._logger.info(f"Final total booked opportunities: {count}")
        return count
