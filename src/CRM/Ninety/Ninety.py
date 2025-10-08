from src.CRM.SmartMoving.Pages.Settings import Settings
from src.CRM.SmartMoving.Pages.Sales import Sales
from src.CRM.CRM import CustomerRelationshipManagementSoftware

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from src.Login.LoginCredentials import LoginCredentials
from src.CRM.SmartMoving.Pages.Calendars import Calendars
from src.CRM.SmartMoving.Pages.Insights import Insights

import os
from datetime import datetime
import traceback


class Ninety(CustomerRelationshipManagementSoftware):
    def __init__(
        self,
        base_url: str,
        login_credentials: LoginCredentials,
        selenium_driver,
    ):
        super().__init__(base_url, login_credentials, selenium_driver)
        self._logger.info("SmartMoving instance initialized.")

