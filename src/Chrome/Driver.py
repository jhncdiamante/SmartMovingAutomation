from src.Chrome.IDriver import IDriver
import undetected_chromedriver as uc

class ChromeDriver(IDriver):
    def __init__(self):
        self._driver = None
        self.chrome_options = uc.ChromeOptions()


    def _set_up_options(self):
        args = [
            "--disable-gpu",
            "--ignore-certificate-errors",
            "--ignore-ssl-errors=yes",
            "--disable-web-security",
            "--allow-running-insecure-content",
            "--log-level=3",
            "--no-sandbox",
            "--enable-unsafe-swiftshader",
            "--disable-dev-shm-usage",
            "--window-size=1920,1080",
            "--disable-browser-side-navigation",
            "--disable-features=VizDisplayCompositor",
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-infobars",
            "--disable-save-password-bubble",
            "--disable-notifications",
            #"--headless",
        ]
        for arg in args:
            self.chrome_options.add_argument(arg)

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    def set_up_driver(self):
        self._set_up_options()
        self._driver = uc.Chrome(options=self.chrome_options, use_subprocess=True)
