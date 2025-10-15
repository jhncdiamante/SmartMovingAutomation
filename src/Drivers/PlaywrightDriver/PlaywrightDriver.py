# src/PlaywrightDriver/PlaywrightDriver.py
from playwright.sync_api import sync_playwright

class PlaywrightDriver:
    def __init__(self, browser_type: str = "chromium", headless: bool = False):
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        self.browser_type = browser_type
        self.headless = headless

    def set_up_driver(self):
        self._playwright = sync_playwright().start()
        browser_launcher = getattr(self._playwright, self.browser_type)
        self._browser = browser_launcher.launch(
            headless=self.headless,
            args=[
                "--disable-gpu",
                "--ignore-certificate-errors",
                "--ignore-ssl-errors=yes",
                "--disable-web-security",
                "--allow-running-insecure-content",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--window-size=1920,1080",
                "--disable-extensions",
                "--disable-infobars",
                "--disable-notifications",
            ]
        )
        self._context = self._browser.new_context()
        self._page = self._context.new_page()

    @property
    def page(self):
        return self._page

    def close(self):
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
