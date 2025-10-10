from src.CRM.CRM import CustomerRelationshipManagementSoftware

from src.CRM.Ninety.Pages.Scorecard import Scorecard
from selenium.webdriver.common.by import By
from src.Login.LoginCredentials import LoginCredentials

class Ninety(CustomerRelationshipManagementSoftware):
    BASE_URL = "https://app.ninety.io/login"
    EMAIL_FIELD_LOCATOR = By.ID, "login-email"
    PASSWORD_FIELD_LOCATOR = By.ID, "login-password"
    LOGIN_BUTTON_LOCATOR = By.ID ,"login-button"

    def __init__(self, login_credentials: LoginCredentials, selenium_driver, scorecard: Scorecard):
        super().__init__(login_credentials, selenium_driver)
        self.scorecard = scorecard
