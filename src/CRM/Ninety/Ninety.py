# src/CRM/Ninety/Ninety.py
from src.CRM.CRM import CustomerRelationshipManagementSoftware
from src.CRM.Ninety.Pages.Scorecard import Scorecard
from src.Login.LoginCredentials import LoginCredentials

import time

class Ninety(CustomerRelationshipManagementSoftware):
    BASE_URL = "https://app.ninety.io/login"

    EMAIL_FIELD_SELECTOR = "#login-email"
    PASSWORD_FIELD_SELECTOR = "#login-password"
    LOGIN_BUTTON_SELECTOR = "#login-button"

    def __init__(self, login_credentials: LoginCredentials, page, scorecard: Scorecard):
        super().__init__(login_credentials, page)
        self.scorecard = scorecard
        self.page = page

    def login(self):
        """Logs into Ninety.io using the provided credentials."""
        self.page.set_default_navigation_timeout(500_000)
        self.page.goto(self.BASE_URL, wait_until="domcontentloaded")

        self.page.wait_for_selector(self.EMAIL_FIELD_SELECTOR)
        self.page.fill(self.EMAIL_FIELD_SELECTOR, self._login_credentials.username)
        self.page.fill(self.PASSWORD_FIELD_SELECTOR, self._login_credentials.password)


        # Wait until post-login navigation completes
        with self.page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
            self.page.click(self.LOGIN_BUTTON_SELECTOR)

        self.page.wait_for_function(
            "document.readyState === 'complete'",
            timeout=60000
        )

        self._logger.info("Successfully logged in.")
        time.sleep(10)
