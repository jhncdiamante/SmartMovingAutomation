from playwright.sync_api import Page as PlaywrightPage
from src.CRM.Page import Page
from src.Helpers.logging_config import setup_logger



class PlaywrightPage(Page):
    DEFAULT_TIMEOUT = 60_000  # milliseconds

    def __init__(self, page: PlaywrightPage):
        self._page = page
        cls = self.__class__
        self._logger = setup_logger(f"{cls.__module__}.{cls.__name__}")
        self._logger.info(f"Initialized {cls.__name__}")
        
    @property
    def _locator(self) -> str:
        """Subclasses must provide their menu XPath"""
        raise NotImplementedError

    def open(self) -> None:
        """Open the page by clicking the element described by _locator."""
        self._logger.info("Opening page...")
        locator = self._page.locator(self._locator)
        locator.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
        locator.click()
        self._page.wait_for_timeout(5000)  # mimic time.sleep(5)

    def _wait_for_complete_loading(self) -> None:
        self._page.wait_for_function(
            "document.readyState === 'complete'",
            timeout=60000
        )