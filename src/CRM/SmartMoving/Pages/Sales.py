
from selenium.webdriver.support.ui import WebDriverWait
from src.Drivers.IDriver import IDriver
from src.CRM.SmartMoving.Pages.SmartMovingPage import SmartMovingPage
from undetected_chromedriver import WebElement
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)
import time
from selenium.webdriver.support import expected_conditions as EC
from src.CRM.SmartMoving.Filters.SalesDashboardFilter import SalesDashboardSalesPersonFilter
from selenium.webdriver.common.by import By
from datetime import datetime

class Sales(SmartMovingPage):
    def __init__(self, route: str, driver: IDriver, sales_dropdown_filter: SalesDashboardSalesPersonFilter):
        super().__init__(route, driver)
        self.salesperson_filter = sales_dropdown_filter

    def _get_count(self, item: str, table_name: str) -> int:
        if table_name == "Open Items":
            # Locate the item_name element's parent's next sibling that contains the respective item count
            xpath = f"//h5[normalize-space(text())='{item}']/parent::div/following-sibling::h2[1]"
        elif table_name == "Actions Taken":
            # Locate the next sibling of item_name element
            xpath = f"//td[normalize-space(text())='{item}']/following-sibling::td[1]"
        else:
            raise ValueError("Invalid table name: ", table_name)

        count_el = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        text = count_el.text.strip()
        return int("".join(filter(str.isdigit, text))) if text else 0

    def get_follow_ups(self) -> int:
        return self._get_count("Follow-ups", "Open Items")
        
    def get_unread_messages(self) -> int:
        return self._get_count("Unread Messages", "Open Items")

    def get_stale_opportunities(self) -> int:
        return self._get_dates("Stale Opportunities")

    def get_inventory_submissions(self) -> int:
        return self._get_dates("Inventory Submissions")

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

    def _get_dates(self, item: str) -> int:
        xpath = f"//h5[normalize-space(text())='{item}']/parent::div"
        item_el = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        item_el.click()

        
        count = 0
        date_today = datetime.today().date()
        while True:
            dates = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "sm-viper-date-time-column-template"))
            )

            i = len(dates) - 1
            while i >= 0:
                date = datetime.strptime(dates[i].text.strip(), "%m/%d/%Y %I:%M %p").date()
                if date != date_today:
                    break
                count += 1
                i-=1
            next_button = self._get_next_button()
            if not next_button:
                break

            li_class = next_button.get_attribute("class") or ""
            if "disabled" in li_class:
                self._logger.info("Reach last page...")

                break
            self._logger.info("Cliking next button")
            next_button.click()
            time.sleep(5)



        close_button = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "modal-close icon-close"))
        )
        close_button.click()

        return count


    def get_emails(self) -> int:
        return self._get_count("Emails", "Actions Taken")
    
    def get_calls(self) -> int:
        return self._get_count("Calls", "Actions Taken")

    def get_texts(self) -> int:
        return self._get_count("Texts", "Actions Taken")

    def get_quotes_sent(self) -> int:
        return self._get_count("Quotes Sent", "Actions Taken")

    


