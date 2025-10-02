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

smartmoving.sales.open()


scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

sheet = client.open("DAILY KPIS") # Replace the parameter string with the actual spreadsheet name 
salespersons = ["Rebecca Perez", "Erik Cairo", "Laina Torsell"]

for salesperson in salespersons:
    smartmoving.sales.salesperson_filter.click()
    smartmoving.sales.salesperson_filter.select_value(salesperson)

    sales_worksheet = sheet.worksheet("Sales") # Replace the parameter string with the actual sheet title
    date_today = date.today().strftime("%Y-%m-%d")

    # Get all dates in column 1
    all_dates = sales_worksheet.col_values(1)  

    try:
        # Check if today's date exists
        row_index = all_dates.index(date_today) + 1 
        # Replace the row
        sales_worksheet.update(f"A{row_index}:J{row_index}", [[
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
        ]])
    except ValueError:
        # Today's date not found, append new row
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