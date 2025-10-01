import os
from src.Login.LoginCredentials import LoginCredentials
from src.Chrome.Driver import SeleniumDriver
from src.CRM.SmartMoving.SmartMoving import SmartMoving
from dotenv import load_dotenv
from src.CRM.SmartMoving.Pages.Calendars import Calendars
from src.CRM.SmartMoving.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter, OfficeCalendarUserFilter

load_dotenv()

SMARTMOVING_USERNAME = os.getenv("SMARTMOVING_USERNAME")
SMARTMOVING_PASSWORD = os.getenv("SMARTMOVING_PASSWORD")

smartmoving_login_credentials = LoginCredentials(username=SMARTMOVING_USERNAME, password=SMARTMOVING_PASSWORD)

chrome = SeleniumDriver()
chrome.set_up_driver()


office_calendar_event_filter = OfficeCalendarEventFilter(driver=chrome.driver)
office_calendar_user_filter = OfficeCalendarUserFilter(driver=chrome.driver)



calendars_page = Calendars(route="https://app.smartmoving.com/calendars/office", driver=chrome.driver,
                office_calendar_event_dropdown_filter=office_calendar_event_filter,
                office_calendar_user_dropdown_filter=office_calendar_user_filter)

smartmoving = SmartMoving(base_url="https://app.smartmoving.com/login", login_credentials=smartmoving_login_credentials,
 selenium_driver=chrome.driver, calendars_page=calendars_page)

smartmoving.login()
calendar_page = smartmoving.calendars

calendar_page.open()

calendar_page.name_filter.click()
calendar_page.name_filter.select_value("Erik Cairo")

calendar_page.event_filter.click()
calendar_page.event_filter.select_value("On-Site Estimate")

card_today = calendar_page.get_card_today()

print(card_today.get_date().strftime("%b %d, %Y"))

for card in calendar_page.get_all_cards():
    if len(card.get_events()) > 0:
        print(card.get_events())

