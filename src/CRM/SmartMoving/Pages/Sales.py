
from selenium.webdriver.support.ui import WebDriverWait
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Pages.SmartMovingPage import SmartMovingPage

from selenium.webdriver.support import expected_conditions as EC
from src.CRM.SmartMoving.SalesDashboardFilter import SalesDashboardSalesPersonFilter
from selenium.webdriver.common.by import By

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
        return self._get_count("Stale Opportunities", "Open Items")

    def get_inventory_submissions(self) -> int:
        return self._get_count("Inventory Submissions", "Open Items")

    def get_emails(self) -> int:
        return self._get_count("Emails", "Actions Taken")
    
    def get_calls(self) -> int:
        return self._get_count("Calls", "Actions Taken")

    def get_texts(self) -> int:
        return self._get_count("Texts", "Actions Taken")

    def get_quotes_sent(self) -> int:
        return self._get_count("Quotes Sent", "Actions Taken")

    


