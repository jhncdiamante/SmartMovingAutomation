
from src.CRM.SmartMoving.Pages.Settings import Settings
from src.CRM.SmartMoving.Pages.Sales import Sales
from src.CRM.CRM import CustomerRelationshipManagementSoftware

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.Login.LoginCredentials import LoginCredentials
from src.CRM.SmartMoving.Pages.Calendars import Calendars
import os
from datetime import datetime
from src.CRM.SmartMoving.Pages.Insights import Insights

class SmartMoving(CustomerRelationshipManagementSoftware):
    
    def __init__(self, base_url: str, login_credentials: LoginCredentials, selenium_driver, calendars_page: Calendars, sales_page: Sales, settings_page: Settings, insights_page: Insights):
        super().__init__(base_url, login_credentials, selenium_driver)
        self.calendars = calendars_page
        self.insights = insights_page
        self.sales = sales_page
        self.settings = settings_page



    def screenshot(self, page_name: str, folder: str = "screenshots"):
        """
        Take a screenshot with filename: YYYY-MM-DD_HH-MM_page_name.png
        Saves to 'folder' directory in the project root.
        """
        os.makedirs(folder, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = os.path.join(folder, f"{timestamp}_{page_name}.png")

        # Take screenshot
        self._driver.save_screenshot(filename)
        return filename

    def _open_url(self, url: str):
        self._driver.get(url)
        self._wait_for_complete_loading()

    def close(self):
        self._driver.quit()

    def login(self):
        self._open_url(self.base_url)
        self._driver.maximize_window()
        self._driver.execute_script("document.body.style.zoom='80%'")
        email_address_form = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.ID, "emailAddress"))
        )
        password_form = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )

        email_address_form.send_keys(self._login_credentials.username)
        password_form.send_keys(self._login_credentials.password)

        sign_in_btn = WebDriverWait(self._driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='sign-in-btn']"))
        )
        sign_in_btn.click()

        
