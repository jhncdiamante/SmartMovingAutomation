
from src.Helpers.logging_config import setup_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



logger = setup_logger(__name__)

def extract_auth_token(driver) -> str | None:
    """Extract auth token directly from localStorage."""
    try:
        print(driver.current_url)
        print(driver.execute_script("return Object.keys(localStorage);"))
        print(driver.execute_script("return localStorage.getItem('SmartMoving.CurrentUser');"))

        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return localStorage.getItem('SmartMoving.CurrentUser') !== null")
        )
        
        token = driver.execute_script("""
            const userData = JSON.parse(localStorage.getItem('SmartMoving.CurrentUser') || '{}');
            return userData?.token || null;
        """)

        logger.info(f"Extracted token: {token}")
        if token:
            logger.info(f"Successfully extracted SmartMoving auth token: {token}")
        else:
            logger.warning("Auth token not found in localStorage.")
        return token
    except Exception as e:
        logger.error(f"Failed to extract auth token: {e}")
        return None