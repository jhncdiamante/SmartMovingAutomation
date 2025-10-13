from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
)

from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.SeleniumDriverumDriverumDriverumDriverumDriver.IDriver import IDriver
from src.CRM.SmartMoving.Filters.AccountingJobRevenueDateTypeFilter import AccountingJobRevenueDateFilter
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter


class AccountingJobRevenue(InsightsPage):

    DEFAULT_TIMEOUT = 60

    def __init__(self, driver: IDriver, date_filter: AccountingJobRevenueDateFilter, calendar_filter: CalendarFilter):
        super().__init__(driver)
        self.date_filter = date_filter
        self.calendar_filter = calendar_filter

    @property
    def _locator(self) -> tuple:
        return By.XPATH, "//a[normalize-space(text())='Accounting Job Revenue']"

    def _wait_for_element(self, locator: tuple, condition=EC.visibility_of_element_located, timeout=None):
        timeout = timeout or self.DEFAULT_TIMEOUT
        try:
            return WebDriverWait(self._driver, timeout).until(condition(locator))
        except TimeoutException:
            self._logger.error(f"Timeout waiting for element: {locator}")
        except WebDriverException as e:
            self._logger.error(f"WebDriver error while waiting for element: {locator} | {e}")
        return None

    def get_net_revenue(self) -> float | None:
        """Extracts and parses the Net Revenue value from the Insights page."""
        xpath = "//td[.//div[normalize-space(text())='Net Revenue (less taxes and tips)']]//following-sibling::td"
        self._logger.info("Locating net revenue value...")

        net_revenue_el = self._wait_for_element((By.XPATH, xpath))
        if not net_revenue_el:
            self._logger.warning("Failed to get net revenue")
            return None

        raw_text = getattr(net_revenue_el, "text", "").strip()
        if not raw_text:
            self._logger.error("Net revenue element text is empty.")
            return None

        self._logger.debug(f"Raw net revenue text: {raw_text}")

        try:
            value = float(raw_text.replace("$", "").replace(",", "").strip())
            self._logger.info(f"Extracted net revenue: {value}")
            return value
        except ValueError:
            self._logger.warning(f"Invalid net revenue format: {raw_text}")
        except Exception as e:
            self._logger.exception(f"Unexpected error parsing net revenue: {e}")

    def open_modal(self, item: str) -> bool:
        """Opens a modal corresponding to a specific metric."""
        item_el_xpath = f"//div[@class='clickable-metric' and normalize-space(text())='{item}']"
        self._logger.info(f"Attempting to open modal for: {item}")

        element = self._wait_for_element((By.XPATH, item_el_xpath), condition=EC.element_to_be_clickable)
        if not element:
            self._logger.warning(f"Failed to open modal {item}.")
            raise Exception

        try:
            element.click()
            self._logger.info(f"Modal for '{item}' opened successfully.")
            return True
        except (StaleElementReferenceException, WebDriverException) as e:
            self._logger.error(f"Failed to click modal element '{item}': {e}")
        except Exception as e:
            self._logger.warning(f"Failed to open modal due to error: {e}")
        
        raise Exception
        


    def close_modal(self) -> bool:
        """Closes the currently open modal if present."""
        selector = "a.modal-close.icon-close"
        element = self._wait_for_element((By.CSS_SELECTOR, selector), condition=EC.element_to_be_clickable)
        if not element:
            self._logger.warning("Unable to locate the close button for modal.")
            return False

        try:
            element.click()
            self._logger.info("Modal closed successfully.")
            return True
        except (StaleElementReferenceException, WebDriverException) as e:
            self._logger.warning(f"Failed to close modal: {e}")
            return False

    def get_number_of_valuation_closed(self) -> int:
        """Returns the number of closed valuations."""
        xpath = "//td[.//sm-viper-text-column-template[normalize-space(text())='Closed']]"
        self._logger.info("Fetching number of closed valuations...")

        elements = self._wait_for_element((By.XPATH, xpath), condition=EC.visibility_of_all_elements_located)
        count = len(elements) if elements else 0
        self._logger.info(f"Found {count} closed valuations.")
        return count

    def get_total_valuation_cost(self) -> float:
        """Calculates the total valuation cost from the modal table."""
        xpath = "//div[@class='modal-body']//table/tbody//tr/td[last()]"
        self._logger.info("Calculating total valuation cost...")

        elements = self._wait_for_element((By.XPATH, xpath), condition=EC.visibility_of_all_elements_located)
        if not elements:
            self._logger.warning("No valuation cost elements found.")
            return 0.0

        total = 0.0
        for el in elements:
            text = el.text.strip().replace("$", "").replace(",", "")
            if not text:
                continue
            try:
                total += float(text)
            except ValueError:
                self._logger.warning(f"Skipping invalid valuation cost value: {text}")

        self._logger.info(f"Total valuation cost: {total}")
        return total
