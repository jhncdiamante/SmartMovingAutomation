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


class SmartMoving(CustomerRelationshipManagementSoftware):
    
    def __init__(
        self,
        base_url: str,
        login_credentials: LoginCredentials,
        selenium_driver,
        calendars_page: Calendars,
        sales_page: Sales,
        settings_page: Settings,
        insights_page: Insights
    ):
        super().__init__(base_url, login_credentials, selenium_driver)
        self.calendars = calendars_page
        self.insights = insights_page
        self.sales = sales_page
        self.settings = settings_page
        self._logger.info("SmartMoving instance initialized.")

    def screenshot(self, page_name: str, folder: str = "screenshots"):
        """Take a screenshot and save it to the given folder."""
        try:
            os.makedirs(folder, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = os.path.join(folder, f"{timestamp}_{page_name}.png")
            self._driver.save_screenshot(filename)
            self._logger.info(f"Screenshot saved: {filename}")
            return filename
        except WebDriverException as e:
            self._logger.error(f"Failed to capture screenshot: {e}", exc_info=True)
            return None
        except Exception as e:
            self._logger.error(f"Unexpected error during screenshot: {e}", exc_info=True)
            return None

    def _open_url(self, url: str):
        """Open a URL with safe error handling."""
        try:
            self._logger.info(f"Navigating to {url}")
            self._driver.get(url)
            self._wait_for_complete_loading()
        except TimeoutException:
            self._logger.error(f"Page load timeout while opening {url}", exc_info=True)
        except WebDriverException as e:
            self._logger.error(f"WebDriver failed to open {url}: {e}", exc_info=True)
        except Exception as e:
            self._logger.error(f"Unexpected error while opening {url}: {e}", exc_info=True)

    def close(self):
        """Safely close the driver."""
        try:
            self._logger.info("Closing CRM...")
            self._driver.quit()
        except WebDriverException as e:
            self._logger.error(f"Error while closing browser: {e}", exc_info=True)
        except Exception as e:
            self._logger.error(f"Unexpected error during close: {e}", exc_info=True)

    def login(self):
        """Perform login with robust error handling."""
        try:
            self._logger.info("Starting login process...")
            self._open_url(self.base_url)
            self._driver.maximize_window()
            self._driver.execute_script("document.body.style.zoom='80%'")

            self._logger.info("Locating email and password form fields...")
            email_field = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "emailAddress"))
            )
            password_field = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.ID, "password"))
            )

            self._logger.info("Entering credentials...")
            email_field.clear()
            password_field.clear()
            email_field.send_keys(self._login_credentials.username)
            password_field.send_keys(self._login_credentials.password)

            self._logger.info("Attempting sign-in...")
            sign_in_btn = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='sign-in-btn']"))
            )
            sign_in_btn.click()

            WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-test-id='sign-in-btn']"))
            )

            self._logger.info("Login successful.")
            return True

        except TimeoutException as e:
            self._logger.error("Login failed: element not found or timed out.", exc_info=True)
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            self._logger.error(f"Login failed due to element issue: {e}", exc_info=True)
        except WebDriverException as e:
            self._logger.error(f"Selenium WebDriver failure during login: {e}", exc_info=True)
        except Exception as e:
            self._logger.critical(f"Unexpected login error: {traceback.format_exc()}")
        return False