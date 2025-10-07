
from src.Helpers.logging_config import setup_logger

logger = setup_logger(__name__)

def extract_auth_token(driver) -> str | None:
    """Extract auth token directly from localStorage."""
    try:
        script = """
            function getUserToken() {
                if (typeof window !== 'undefined') {
                    const userData = JSON.parse(localStorage.getItem('SmartMoving.CurrentUser') || '{}');
                    return userData.token || null;
                }
                return null;
            }

            getUserToken();

        """
        token = driver.execute_script(script)
        if token:
            logger.info("Successfully extracted SmartMoving auth token.")
        else:
            logger.warning("Auth token not found in localStorage.")
        return token
    except Exception as e:
        logger.error(f"Failed to extract auth token: {e}")
        return None