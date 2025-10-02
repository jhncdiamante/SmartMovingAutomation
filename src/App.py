import os
from src.Login.LoginCredentials import LoginCredentials
from src.Chrome.Driver import ChromeDriver
from src.CRM.SmartMoving.SmartMoving import SmartMoving
from dotenv import load_dotenv
from src.CRM.SmartMoving.Pages.Calendars import Calendars
from src.CRM.SmartMoving.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter, OfficeCalendarUserFilter
from src.CRM.SmartMoving.Pages.Sales import Sales
from datetime import timedelta, date
from src.CRM.SmartMoving.SalesDashboardFilter import SalesDashboardSalesPersonFilter
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials
load_dotenv()

SMARTMOVING_USERNAME = os.getenv("SMARTMOVING_USERNAME")
SMARTMOVING_PASSWORD = os.getenv("SMARTMOVING_PASSWORD")

smartmoving_login_credentials = LoginCredentials(username=SMARTMOVING_USERNAME, password=SMARTMOVING_PASSWORD)

chrome = ChromeDriver()
chrome.set_up_driver()


office_calendar_event_filter = OfficeCalendarEventFilter(driver=chrome.driver)
office_calendar_user_filter = OfficeCalendarUserFilter(driver=chrome.driver)

calendars_page = Calendars(route="https://app.smartmoving.com/calendars/office", driver=chrome.driver,
                office_calendar_event_dropdown_filter=office_calendar_event_filter,
                office_calendar_user_dropdown_filter=office_calendar_user_filter)

sales_filter = SalesDashboardSalesPersonFilter(driver=chrome.driver)


sales_page = Sales(route="https://app.smartmoving.com/sales/dashboard", driver=chrome.driver,
                    sales_dropdown_filter=sales_filter)

smartmoving = SmartMoving(base_url="https://app.smartmoving.com/login", login_credentials=smartmoving_login_credentials,
 selenium_driver=chrome.driver, calendars_page=calendars_page, sales_page=sales_page)

smartmoving.login()

time.sleep(5)


smartmoving.calendars.open()

smartmoving.calendars.name_filter.click()
smartmoving.calendars.name_filter.select_value("Erik Cairo")

smartmoving.calendars.event_filter.click()
smartmoving.calendars.event_filter.select_value("On-Site Estimate")

card_today = smartmoving.calendars.get_card_today()


scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

sheet = client.open("DAILY KPIS")

calendar_worksheet = sheet.worksheet("Office Calendar")

date_tomorrow = (card_today.get_date() + timedelta(days=1)).strftime("%Y-%m-%d")

calendar_worksheet.append_row([
    date_tomorrow,
    len(card_today.get_events()),
    ""
])         


smartmoving.sales.open()


salespersons = ["Rebecca Perez", "Erik Cairo", "Laina Torsell"]

for salesperson in salespersons:

    smartmoving.sales.salesperson_filter.click()
    smartmoving.sales.salesperson_filter.select_value(salesperson)

    sales_worksheet = sheet.worksheet("Sales")
    date_today = date.today().strftime("%Y-%m-%d") # e.g. 2025-07-23 format
    sales_worksheet.append_row([
        date_today,
        smartmoving.sales.get_calls(),
        smartmoving.sales.get_emails(),
        smartmoving.sales.get_texts(),
        smartmoving.sales.get_quotes_sent(),
        smartmoving.sales.get_follow_ups(),
        smartmoving.sales.get_unread_messages(),
        smartmoving.sales.get_stale_opportunities(),
        smartmoving.sales.get_inventory_submissions(),
        salesperson
    ])
