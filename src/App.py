import os
from src.Login.LoginCredentials import LoginCredentials
from src.Chrome.Driver import SeleniumDriver
from src.CRM.SmartMoving.SmartMoving import SmartMoving
from dotenv import load_dotenv
from src.CRM.SmartMoving.Pages.Calendars import Calendars
from src.CRM.SmartMoving.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter, OfficeCalendarUserFilter
from src.CRM.SmartMoving.Pages.Sales import Sales

from src.CRM.SmartMoving.SalesDashboardFilter import SalesDashboardSalesPersonFilter

load_dotenv()

SMARTMOVING_USERNAME = os.getenv("SMARTMOVING_USERNAME")
SMARTMOVING_PASSWORD = os.getenv("SMARTMOVING_PASSWORD")

smartmoving_login_credentials = LoginCredentials(username=SMARTMOVING_USERNAME, password=SMARTMOVING_PASSWORD)

chrome = SeleniumDriver()
chrome.set_up_driver()


office_calendar_event_filter = OfficeCalendarEventFilter(driver=chrome.driver)
office_calendar_user_filter = OfficeCalendarUserFilter(driver=chrome.driver)
sales_filter = SalesDashboardSalesPersonFilter(driver=chrome.driver)



calendars_page = Calendars(route="https://app.smartmoving.com/calendars/office", driver=chrome.driver,
                office_calendar_event_dropdown_filter=office_calendar_event_filter,
                office_calendar_user_dropdown_filter=office_calendar_user_filter)

sales_page = Sales(route="https://app.smartmoving.com/sales/dashboard", driver=chrome.driver,
                    sales_dropdown_filter=sales_filter)

smartmoving = SmartMoving(base_url="https://app.smartmoving.com/login", login_credentials=smartmoving_login_credentials,
 selenium_driver=chrome.driver, calendars_page=calendars_page, sales_page=sales_page)

smartmoving.login()
import time
time.sleep(10)
calendar_page = smartmoving.calendars

calendar_page.open()

calendar_page.name_filter.click()
calendar_page.name_filter.select_value("Erik Cairo")

calendar_page.event_filter.click()
calendar_page.event_filter.select_value("On-Site Estimate")

card_today = calendar_page.get_card_today()

print(card_today.get_date().strftime("%b %d, %Y"))
print(card_today.get_events())

sales_page = smartmoving.sales

sales_page.open()

print(f"Emails: {sales_page.get_emails()}")
print(f"Calls: {sales_page.get_calls()}")

print(f"Texts: {sales_page.get_texts()}")

print(f"Quotes Sent: {sales_page.get_quotes_sent()}")
print(f"Follow ups: {sales_page.get_follow_ups()}")

print(f"Inventory Submissions: {sales_page.get_inventory_submissions()}")

print(f"Unread Messages: {sales_page.get_unread_messages()}")

print(f"Stale Opportunites: {sales_page.get_stale_opportunities()}")


smartmoving.close()



