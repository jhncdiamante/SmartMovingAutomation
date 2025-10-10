import os
import time
from datetime import date
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

from src.Login.LoginCredentials import LoginCredentials
from src.Chrome.Driver import ChromeDriver
from src.CRM.SmartMoving.SmartMoving import SmartMoving
from src.CRM.SmartMoving.Pages.Calendars import Calendars
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter, OfficeCalendarUserFilter
from src.CRM.SmartMoving.Pages.Sales import Sales
from src.CRM.SmartMoving.Filters.SalesDashboardFilter import SalesDashboardSalesPersonFilter
import logging
# Configure logging
logging.basicConfig(
    filename="app.log",      
    level=logging.ERROR,      
    format="%(asctime)s [%(levelname)s] %(message)s"
)
load_dotenv()
SMARTMOVING_USERNAME = os.getenv("SMARTMOVING_USERNAME")
SMARTMOVING_PASSWORD = os.getenv("SMARTMOVING_PASSWORD")

smartmoving_login_credentials = LoginCredentials(username=SMARTMOVING_USERNAME, password=SMARTMOVING_PASSWORD)

chrome = ChromeDriver()
chrome.set_up_driver()

office_calendar_event_filter = OfficeCalendarEventFilter(driver=chrome.driver)
office_calendar_user_filter = OfficeCalendarUserFilter(driver=chrome.driver)

calendars_page = Calendars(
    route="https://app.smartmoving.com/calendars/office",
    driver=chrome.driver,
    office_calendar_event_dropdown_filter=office_calendar_event_filter,
    office_calendar_user_dropdown_filter=office_calendar_user_filter
)

sales_filter = SalesDashboardSalesPersonFilter(driver=chrome.driver)
sales_page = Sales(route="https://app.smartmoving.com/sales/dashboard", driver=chrome.driver, sales_dropdown_filter=sales_filter)

smartmoving = SmartMoving(
    login_credentials=smartmoving_login_credentials,
    selenium_driver=chrome.driver,
    calendars_page=calendars_page,
    sales_page=sales_page
)

smartmoving.login()
time.sleep(5)
smartmoving.sales.open()

# -----------------------------
# Google Sheets Setup
# -----------------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

sheet = client.open("DAILY KPIS") 
sales_worksheet = sheet.worksheet("agent-dashboard") 

date_today = date.today().strftime("%Y-%m-%d")
salespersons = ["Rebecca Perez", "Erik Cairo", "Laina Torsell"]

existing_data = sales_worksheet.get_all_values()
columns = existing_data[0]  # header row
df = pd.DataFrame(existing_data[1:], columns=columns)

for salesperson in salespersons:
    smartmoving.sales.salesperson_filter.click()
    smartmoving.sales.salesperson_filter.select_value(salesperson)
    time.sleep(5)
    smartmoving.screenshot(page_name=f"sales_{salesperson}")

    # Create new data row
    new_row = {
        "Date": date_today,
        "Calls": smartmoving.sales.get_calls() or 0,
        "Emails": smartmoving.sales.get_emails() or 0,
        "Texts": smartmoving.sales.get_texts() or 0,
        "Quotes Sent": smartmoving.sales.get_quotes_sent() or 0,
        "Follow Ups": smartmoving.sales.get_follow_ups() or 0,
        "Unread Messages": smartmoving.sales.get_unread_messages() or 0,
        "Stale Opportunities": smartmoving.sales.get_stale_opportunities() or 0,
        "Inventory Submissions": smartmoving.sales.get_inventory_submissions() or 0,
        "Salesperson": salesperson
    }

    # Check if this date + salesperson already exists
    mask = (df["Date"] == date_today) & (df["Salesperson"] == salesperson)
    if mask.any():
        for col, val in new_row.items():
            df.loc[mask, col] = val
    else:
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

df.to_csv("sales_worksheet_backup.csv", index=False)
sales_worksheet.clear()
time.sleep(3)

try:
    # Update header
    sales_worksheet.append_row(df.columns.tolist())
    # Update all data in one batch
    sales_worksheet.append_rows(df.values.tolist())
except Exception as e:
    logging.error(f"An error occured while updating the table: {e}")

