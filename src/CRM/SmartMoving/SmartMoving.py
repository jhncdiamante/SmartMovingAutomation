
from src.CRM.SmartMoving.Pages.Sales import Sales
from src.CRM.CRM import CustomerRelationshipManagementSoftware

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.Login.LoginCredentials import LoginCredentials
from src.CRM.SmartMoving.Pages.Calendars import Calendars

class SmartMoving(CustomerRelationshipManagementSoftware):
    
    def __init__(self, base_url: str, login_credentials: LoginCredentials, selenium_driver, calendars_page: Calendars, sales_page: Sales):
        super().__init__(base_url, login_credentials, selenium_driver)
        self.calendars = calendars_page
        #self.insights = insights_page
        self.sales = sales_page
        #self.settings = settings_page

    def _open_url(self, url: str):
        self._driver.get(url)
        self._wait_for_complete_loading()

    def close(self):
        self._driver.quit()

    def login(self):
        self._open_url(self.base_url)
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
        self._wait_for_complete_loading()

        
