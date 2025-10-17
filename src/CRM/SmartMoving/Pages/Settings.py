from src.CRM.SmartMoving.Pages.SmartMovingPage import SmartMovingPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Settings(SmartMovingPage):
    def get_all_crew_members(self) -> list[str]:
        self._driver.get("https://app.smartmoving.com/settings/crew-members")
        crew_member_name_els = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "td:first-child > a"))
        )

        # Extract text (names)
        crew_member_names = [el.text.strip() for el in crew_member_name_els if el.text.strip()]
        return crew_member_names