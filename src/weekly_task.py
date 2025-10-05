import os
import time
from datetime import date
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from src.Login.LoginCredentials import LoginCredentials
from src.Chrome.Driver import ChromeDriver
from src.CRM.SmartMoving.SmartMoving import SmartMoving
from src.CRM.SmartMoving.Pages.Calendars import Calendars
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter, OfficeCalendarUserFilter
from src.CRM.SmartMoving.Pages.Sales import Sales
from src.CRM.SmartMoving.Filters.SalesDashboardFilter import SalesDashboardSalesPersonFilter
import logging 
from src.CRM.SmartMoving.Pages.Settings import Settings
from src.CRM.SmartMoving.Pages.InsightsPage.BookOpportunitiesByDateBooked import BookedOpportunitiesByDateBooked

from src.CRM.SmartMoving.Pages.Insights import Insights
from src.CRM.SmartMoving.Pages.InsightsPage.AccountingJobRevenue import AccountingJobRevenue
from src.CRM.SmartMoving.Filters.AccountingJobRevenueDateTypeFilter import AccountingJobRevenueDateFilter
from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.CRM.SmartMoving.Filters.SidePanelFilter import SidePanelFilter

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

settings_page = Settings(route="https://app.smartmoving.com/settings", driver=chrome.driver)

accounting_job_revenue_date_filter = AccountingJobRevenueDateFilter(driver=chrome.driver)
calendar_filter = CalendarFilter(driver=chrome.driver)
side_panel_filter = SidePanelFilter(driver=chrome.driver)

insights_page = Insights(route="https://app.smartmoving.com/reports/smart-insights/lists", driver=chrome.driver,
                         accounting_job_revenue=AccountingJobRevenue(driver=chrome.driver, date_filter=accounting_job_revenue_date_filter, calendar_filter=calendar_filter),
                         booked_opportunities_by_date_booked=BookedOpportunitiesByDateBooked(driver=chrome.driver, calendar_filter=calendar_filter, side_panel_filter=side_panel_filter),
                         #booking_percent_by_survey_type=InsightsPage(driver=chrome.driver),
                         #accounting_storage_revenue=InsightsPage(driver=chrome.driver),
                         #completed_moves=InsightsPage(driver=chrome.driver),
                         #booked_opportunities_by_service_date=InsightsPage(driver=chrome.driver),
                         #outstanding_balances=InsightsPage(driver=chrome.driver),
                         #salesperson_performance=InsightsPage(driver=chrome.driver),
                         #lost_leads_and_opportunities_summary=InsightsPage(driver=chrome.driver),
                         #estimate_accuracy_summary=InsightsPage(driver=chrome.driver)
                         )



smartmoving = SmartMoving(
    base_url="https://app.smartmoving.com/login",
    login_credentials=smartmoving_login_credentials,
    selenium_driver=chrome.driver,
    calendars_page=calendars_page,
    sales_page=sales_page,
    settings_page=settings_page,
    insights_page=insights_page
)

smartmoving.login()
time.sleep(5)

# Get all creww members

#smartmoving.settings.open()

crew_members = smartmoving.settings.get_all_crew_members()

number_of_drivers = len([member_name for member_name in crew_members if member_name and "(D)" in member_name])
number_of_movers = len([member_name for member_name in crew_members if member_name and "(D)(CL)" not in member_name])

print(f"Number of Drivers: {number_of_drivers}")
print(f"Number of Movers: {number_of_movers}")

smartmoving.insights.open()
smartmoving.insights.accounting_job_revenue.open()
smartmoving.insights.accounting_job_revenue.date_filter.click()
smartmoving.insights.accounting_job_revenue.date_filter.select_value("Closed Date")
time.sleep(2)
smartmoving.insights.accounting_job_revenue.calendar_filter.click()
smartmoving.insights.accounting_job_revenue.calendar_filter.select_value('This Week')

net_revenue = smartmoving.insights.accounting_job_revenue.get_net_revenue()

print(f"Net Revenue: {net_revenue}")

smartmoving.insights.accounting_job_revenue.close()

smartmoving.insights.booked_opportunities_by_date_booked.open()
time.sleep(3)

smartmoving.insights.booked_opportunities_by_date_booked.calendar_filter.click()
time.sleep(3)

smartmoving.insights.booked_opportunities_by_date_booked.calendar_filter.select_value('This Week')
time.sleep(3)


total_estimated_amount = smartmoving.insights.booked_opportunities_by_date_booked.get_total_estimated_amount()
time.sleep(3)


print(f"Booked Opportunities Total Estimated Amount: {total_estimated_amount}")
smartmoving.insights.booked_opportunities_by_date_booked.side_panel_filter.click()
time.sleep(3)

smartmoving.insights.booked_opportunities_by_date_booked.side_panel_filter.select_value(filter_type="Sales Person", selected_values=["Erik Cairo"])
time.sleep(3)

smartmoving.insights.booked_opportunities_by_date_booked.side_panel_filter.apply()
smartmoving.insights.booked_opportunities_by_date_booked.side_panel_filter.close()
time.sleep(3)

total_booked_count = smartmoving.insights.booked_opportunities_by_date_booked.get_total_booked_count()

print(f"Total Booked Count: {total_booked_count}")
time.sleep(3000)







