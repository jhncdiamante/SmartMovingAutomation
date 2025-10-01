
from selenium.webdriver.support.ui import WebDriverWait
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Pages import SmartMovingPage
from src.CRM.SmartMoving.SalesDashboardFilter import SalesDashboardSalesPersonFilter
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Sales(SmartMovingPage):
    def __init__(self, route: str, driver: IDriver, office_calendar_event_dropdown_filter: SalesDashboardSalesPersonFilter):
        super().__init__(route, driver)
        self.salesperson_filter = office_calendar_event_dropdown_filter

    def _get_actions_count_today(self, action: str) -> int:
        xpath = f"//td[normalize-space(text())='{action}']/following-sibling::td[1]"
        count_el = WebDriverWait(self._driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        text = count_el.text.strip()
        return int("".join(filter(str.isdigit, text))) if text else 0

    def get_emails(self) -> int:
        return self._get_actions_count_today("Emails")
    
    def get_calls(self) -> int:
        return self._get_actions_count_today("Calls")

    def get_texts(self) -> int:
        return self._get_actions_count_today("Texts")

    def get_quotes_sent(self) -> int:
        return self._get_actions_count_today("Quotes Sent")

    


