from src.CRM.SmartMoving.Pages.Settings import Settings
from src.CRM.SmartMoving.Pages.Sales import Sales
from src.CRM.CRM import CustomerRelationshipManagementSoftware
from selenium.webdriver.common.by import By

from selenium.common.exceptions import (
    WebDriverException,
)
from src.Login.LoginCredentials import LoginCredentials
from src.CRM.SmartMoving.Pages.Calendars import Calendars
from src.CRM.SmartMoving.Pages.Insights import Insights

import os
from datetime import datetime
import traceback


class SmartMoving(CustomerRelationshipManagementSoftware):
    LOGIN_BUTTON_LOCATOR = By.CSS_SELECTOR, "button[data-test-id='sign-in-btn']"
    EMAIL_FIELD_LOCATOR = By.ID, "emailAddress"
    PASSWORD_FIELD_LOCATOR = By.ID, "password"
    BASE_URL = "https://app.smartmoving.com/login"
    def __init__(
        self,
        login_credentials: LoginCredentials,
        selenium_driver,
        calendars_page: Calendars,
        sales_page: Sales,
        settings_page: Settings,
        insights_page: Insights
    ):
        super().__init__(login_credentials, selenium_driver)
        self.calendars = calendars_page
        self.insights = insights_page
        self.sales = sales_page
        self.settings = settings_page
        self._logger.info("SmartMoving instance initialized.")


    