
from abc import ABC
from src.Login.LoginCredentials import LoginCredentials
from selenium.webdriver.support.ui import WebDriverWait
from src.Helpers.logging_config import setup_logger
import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
import os

from datetime import datetime

class CustomerRelationshipManagementSoftware(ABC):
    DEFAULT_TIMEOUT = 60
    def __init__(self, login_credentials: LoginCredentials, selenium_driver):
        self._login_credentials = login_credentials
        self._driver = selenium_driver
        cls = self.__class__
        self._logger = setup_logger(f"{cls.__module__}.{cls.__name__}")
        self._logger.info(f"Initialized {cls.__name__}")

    @property
    def BASE_URL(self): pass

    @property
    def EMAIL_FIELD_LOCATOR(self): pass
    @property
    def PASSWORD_FIELD_LOCATOR(self): pass
    @property
    def LOGIN_BUTTON_LOCATOR(self): pass


    def open(self):
        self._driver.maximize_window()
        self._driver.get(self.base_url)
        self._wait_for_complete_loading()


    def _wait_for_complete_loading(self, timeout=60):
        WebDriverWait(self._driver, timeout).until(
            lambda _: self._driver.execute_script("return document.readyState")
            == "complete"
        )

    def close(self):
        """Safely close the driver."""
        try:
            self._logger.info("Closing CRM...")
            self._driver.quit()
        except Exception as e:
            self._logger.error(f"Unexpected error during close: {e}", exc_info=True)


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

    
    

    def login(self):
        try:
            self._logger.info("Starting login process...")
            self._open_url(self.BASE_URL)
            self._driver.maximize_window()
            self._driver.execute_script("document.body.style.zoom='80%'")

            self._logger.info("Locating email and password form fields...")
            email_field = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located(self.EMAIL_FIELD_LOCATOR)
            )
            password_field = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located(self.PASSWORD_FIELD_LOCATOR)
            )

            self._logger.info("Entering credentials...")
            email_field.clear()
            password_field.clear()
            email_field.send_keys(self._login_credentials.username)
            password_field.send_keys(self._login_credentials.password)

            self._logger.info("Attempting sign-in...")
            sign_in_btn = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.LOGIN_BUTTON_LOCATOR)
            )
            sign_in_btn.click()

            WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until_not(
                EC.presence_of_element_located(self.LOGIN_BUTTON_LOCATOR)
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
