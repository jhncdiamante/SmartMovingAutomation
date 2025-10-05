from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Chrome.IDriver import IDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SalespersonPerformance(InsightsPage):
    def __init__(self):
        pass

    def get_bad_leads(self) -> int:
        xpath = "//span[normalize-space(text())='Bad']/following-sibling::h2/span[1]"
        bad_leads_el = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return int(bad_leads_el.text.strip())


    def get_bad_leads_percentage(self) -> str:
        xpath = "//span[normalize-space(text())='Bad']/following-sibling::h2/span[2]"
        bad_leads_percentage_el = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return bad_leads_percentage_el.text.strip()


        