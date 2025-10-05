
from selenium.webdriver.support.ui import WebDriverWait
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Pages.SmartMovingPage import SmartMovingPage

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

        count_el = WebDriverWait(self._driver, 60).until(
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

    def _get_dates(self, item: str) -> int:
        xpath = f"//h5[normalize-space(text())='{item}']/parent::div"
        item_el = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        item_el.click()

        dates = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "sm-viper-date-time-column-template"))
        )

        close_button = WebDriverWait(self._driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "modal-close icon-close"))
        )
        close_button.click()

        return len([
            el for el in dates
            if datetime.strptime(el.text.strip(), "%m/%d/%Y %I:%M %p").date() == datetime.today().date()
        ])


    def get_emails(self) -> int:
        return self._get_count("Emails", "Actions Taken")
    
    def get_calls(self) -> int:
        return self._get_count("Calls", "Actions Taken")

    def get_texts(self) -> int:
        return self._get_count("Texts", "Actions Taken")

    def get_quotes_sent(self) -> int:
        return self._get_count("Quotes Sent", "Actions Taken")

    


