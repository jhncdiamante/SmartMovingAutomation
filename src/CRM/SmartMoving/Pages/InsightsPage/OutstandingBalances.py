
from selenium.webdriver.common.by import By
from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OutstandingBalances(InsightsPage):
    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Outstanding Balances']")

    
    def get_total_balance(self) -> float:
        xpath = "//table/tbody/tr/td[last()]"

        balances = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath))
        )

        total_balance = sum([float(balance.text.replace("$", "").replace(",", "").strip()) for balance in balances if balance.text.strip()])

        return total_balance

    