from src.CRM.Features.DropdownFilter import DropdownFilter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OfficeCalendarEventFilter(DropdownFilter):

    def click(self):
        dropdown = WebDriverWait(self._driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='display-value' and normalize-space(text())='Any Type']")))
        dropdown.click()
        WebDriverWait(self._driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ngb-popover-window.popover.show")))

    @property
    def options(self):
        raise NotImplementedError


    def select_value(self, target: str):
        target_xpath = f"//div[@class='label mr-auto' and normalize-space(text())='{target}']"
        target_el = WebDriverWait(self._driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, target_xpath))
        )
        target_el.click()
 
class OfficeCalendarUserFilter(OfficeCalendarEventFilter):
    def click(self):
        dropdown = WebDriverWait(self._driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='display-value' and normalize-space(text())='Any User']")))
        dropdown.click()
        WebDriverWait(self._driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ngb-popover-window.popover.show")))


