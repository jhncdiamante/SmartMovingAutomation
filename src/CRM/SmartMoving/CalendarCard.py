from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.remote.webelement import WebElement

class Card:
    def __init__(self, element: WebElement):
        self._element = element

    def get_events(self) -> list[WebElement]:
        event_body = self._element.find_element(By.CSS_SELECTOR, "div.events")
        return [div.text.strip() for div in event_body.find_elements(By.TAG_NAME, "div")]

    def get_date(self):
        href = self._element.get_attribute("href")
        date_str = href.split("/")[-1]  # "20251001"
        return datetime.strptime(date_str, "%Y%m%d").date()