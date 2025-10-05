from src.CRM.SmartMoving.CalendarCard import Card
from src.CRM.SmartMoving.Pages.SmartMovingPage import SmartMovingPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter, OfficeCalendarUserFilter

class Calendars(SmartMovingPage):
    def __init__(self, route: str, driver: IDriver, office_calendar_event_dropdown_filter: OfficeCalendarEventFilter, office_calendar_user_dropdown_filter: OfficeCalendarUserFilter):
        super().__init__(route, driver)
        self.event_filter = office_calendar_event_dropdown_filter
        self.name_filter = office_calendar_user_dropdown_filter

    def get_card_today(self) -> Card:
        card_el = WebDriverWait(self._driver, 60).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "a.card.today")
        ))

        return Card(element=card_el)

    def get_all_cards(self) -> list[Card]:
        card_els = WebDriverWait(self._driver, 60).until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "a.card")
        ))

        return [Card(card_el) for card_el in card_els]
        
