import time
import requests
from datetime import date, timedelta
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
from src.Drivers.IDriver import IDriver
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from src.CRM.SmartMoving.Filters.SidePanelFilter import SidePanelFilter

from src.CRM.SmartMoving.API import extract_auth_token
from src.CRM.SmartMoving.API import BOOKED_OPP_BY_DATE_BOOKED_PAGE_API_URL
class BookedOpportunitiesByDateBooked(InsightsPage):


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
        xpath = "//span[normalize-space(text())='Estimated Amount']//following-sibling::h2/span[1]"
        self._logger.info("Locating 'Estimated Amount' element...")

        element = self._safe_wait((By.XPATH, xpath), EC.visibility_of_element_located)
        if not element:
            self._logger.warning("Failed to locate Estimated Amount element.")
            return None

        raw_text = (element.text or "").strip()
        if not raw_text or raw_text == "--":
            self._logger.warning("No estimated amount available ('--' or empty).")
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

    def get_total_estimated_amount_prior_year(self) -> float | None:
        """Fetch total estimated amount for the same week last year via API."""
        auth_token = extract_auth_token(self._driver)
        try:
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            try:
                last_year_start = start_of_week.replace(year=start_of_week.year - 1)
                last_year_end = end_of_week.replace(year=end_of_week.year - 1)
            except ValueError:
                last_year_start = (start_of_week - timedelta(days=1)).replace(year=start_of_week.year - 1)
                last_year_end = (end_of_week - timedelta(days=1)).replace(year=end_of_week.year - 1)

            start_iso = f"{last_year_start.isoformat()}T00:00:00.000+08:00"
            end_iso = f"{last_year_end.isoformat()}T23:59:59.999+08:00"

            payload = {
                "parameters": [
                    {
                        "filterType": "DateRange",
                        "dateFilterType": "DateBooked",
                        "quickFilter": None,
                        "startDateUtc": start_iso,
                        "endDateUtc": end_iso,
                        "allowMultipleDays": True
                    },
                    {"filterType": "ReferralSource", "filterMode": "AnyOf", "referralSourceIds": []},
                    {"filterType": "SalesPerson", "filterMode": "AnyOf", "salesPersonIds": []},
                    {"filterType": "Branch", "filterMode": "AnyOf", "branchIds": []},
                    {"filterType": "Estimator", "filterMode": "AnyOf", "estimatorIds": []},
                    {"filterType": "OpportunityTags", "filterMode": "AnyOf", "tags": []},
                    {"filterType": "Affiliate", "filterMode": "AnyOf", "affiliateIds": []}
                ]
            }


            self._logger.info(f"PAYLOAD: {payload}")

            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://app.smartmoving.com",
                "Referer": "https://app.smartmoving.com/",
            }

            self._logger.info(f"Requesting last-year data for {last_year_start} – {last_year_end}...")
            response = requests.post(f"{BOOKED_OPP_BY_DATE_BOOKED_PAGE_API_URL}/visualizations", headers=headers, json=payload, timeout=30)

            
            if response.status_code != 200:
                self._logger.warning(f"API request failed ({response.status_code}): {response.text}")
                return None

            data = response.json()
            primary_values = [item["primaryValue"] for item in data if "primaryValue" in item]
            value = primary_values[2]
            self._logger.info(f"Last year total estimated amount: {value}")
            return float(value)
        except Exception as e:
            self._logger.warning(f"Error fetching last year estimated amount: {e}")
            return None
