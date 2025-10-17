from src.Drivers.IDriver import IDriver
import undetected_chromedriver as uc
from selenium.webdriver import Edge, EdgeOptions

class ChromeDriver(IDriver):
    def __init__(self, headless=True):
        self._driver = None
        self.chrome_options = uc.ChromeOptions()
        self._headless = headless


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
            "--disable-browser-side-navigation",
            "--disable-features=VizDisplayCompositor",
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-infobars",
            "--disable-save-password-bubble",
            "--disable-notifications",
            "--window-size=1920,1080"
            
        ]
        
        for arg in args:
            self.chrome_options.add_argument(arg)

        if self._headless:
            self.chrome_options.add_argument("--headless=new")


        prefs = {"credentials_enable_service": False,
            "profile.password_manager_enabled": False}
        self.chrome_options.add_experimental_option("prefs", prefs)

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    def set_up_driver(self):
        self._set_up_options()
        self._driver = uc.Chrome(options=self.chrome_options, use_subprocess=True)


class EdgeDriver(IDriver):
    def __init__(self):
        self._driver = None
        self.edge_options = EdgeOptions()

    def _set_up_options(self):
        args = [
            "--disable-gpu",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--window-size=1920,1080",
        ]
        for arg in args:
            self.edge_options.add_argument(arg)

    def set_up_driver(self):
        self._set_up_options()
        self._driver = Edge(options=self.edge_options)

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver
