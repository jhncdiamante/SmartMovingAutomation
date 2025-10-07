import os
import time
from datetime import date
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

from src.CRM.SmartMoving.Filters import QuickDateFilter
from src.CRM.SmartMoving.Filters.SalespersonPerformanceDateTypeFilter import SalespersonPerformanceDateTypeFilter
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from src.CRM.SmartMoving.Pages.InsightsPage.CompletedMoves import CompletedMoves
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
from src.CRM.SmartMoving.Pages.InsightsPage.BookOpportunitiesByServiceDate import BookedOpportunitiesByServiceDate

from src.CRM.SmartMoving.Pages.InsightsPage.AccountingStorageRevenue import AccountingStorageRevenue
from src.CRM.SmartMoving.Pages.InsightsPage.BookingPercentBySurveyType import BookingPercentBySurveyType
from src.CRM.SmartMoving.Pages.InsightsPage.EstimateAccuracySummary import EstimateAccuracySummary
from src.CRM.SmartMoving.Pages.InsightsPage.LostLeadsAndOpportunitiesSummary import LostLeadsAndOpportunitiesSummary
from src.CRM.SmartMoving.Pages.InsightsPage.OutstandingBalances import OutstandingBalances
from src.CRM.SmartMoving.Pages.InsightsPage.SalespersonPerformance import SalespersonPerformance
from src.CRM.SmartMoving.Filters.QuickDateFilter import QuickDateFilter
from src.CRM.SmartMoving.Filters.LostLeadsAndOpportunitiesSummaryDateFilter import LostLeadsAndOpportunitiesSummaryDateFilter

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
quick_date_filter = QuickDateFilter(driver=chrome.driver)
salesperson_performance_date_type_filter = SalespersonPerformanceDateTypeFilter(driver=chrome.driver)
lost_leads_and_opp_date_type_filter = LostLeadsAndOpportunitiesSummaryDateFilter(driver=chrome.driver)


insights_page = Insights(route="https://app.smartmoving.com/reports/smart-insights/lists", driver=chrome.driver,
                         accounting_job_revenue=AccountingJobRevenue(driver=chrome.driver, date_filter=accounting_job_revenue_date_filter, calendar_filter=calendar_filter),
                         booked_opportunities_by_date_booked=BookedOpportunitiesByDateBooked(driver=chrome.driver, calendar_filter=calendar_filter, side_panel_filter=side_panel_filter),
                         booking_percent_by_survey_type=BookingPercentBySurveyType(driver=chrome.driver, calendar_filter=calendar_filter),
                         accounting_storage_revenue=AccountingStorageRevenue(driver=chrome.driver, quick_date_filter=quick_date_filter),
                         booked_opportunities_by_service_date=BookedOpportunitiesByServiceDate(driver=chrome.driver, calendar_filter=calendar_filter, side_panel_filter=side_panel_filter),
                         outstanding_balances=OutstandingBalances(driver=chrome.driver, calendar_filter=calendar_filter),
                         salesperson_performance=SalespersonPerformance(driver=chrome.driver, calendar_filter=calendar_filter, date_type_filter="", side_panel_filter=side_panel_filter),
                         lost_leads_and_opportunities_summary=LostLeadsAndOpportunitiesSummary(driver=chrome.driver, calendar_filter=calendar_filter, date_filter=lost_leads_and_opp_date_type_filter),
                         estimate_accuracy_summary=EstimateAccuracySummary(driver=chrome.driver, calendar_filter=calendar_filter),
                         completed_moves=CompletedMoves(driver=chrome.driver), calendar_filter=calendar_filter
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

new_row = {
    "Date": None,
    "Weekly Total Revenue": None,
    "Accounting Job Revenue": None,
    "Accounting Storage Revenue": None,
    "$ Booked Sales": None,
    "YoY Net Lead Growth %": None,
    "Erik Booking % On Site": None,
    "No Survey": None,
    "Valuation on 30% of jobs": None,
    "Average Ticket Amount": None,
    "Booked $ Next Month vs Forecast": None,
    "Aging A/R": None,
    "Completed Moves": None,
    "Valuation as % of Revenue": None,
    "$ Booked PY": None,
    "YoY Booking ($)": None,
    "# Leads PY": None,
    "# Leads CY": None,
    "Bad Leads %": None,
    "Lost leads & opportunities from pricing": None,
    "# of movers": None,
    "# of drivers": None,
    "Erik Total Booked $": None,
    "Erik # of Booked": None,
    "Erik # of Estimates": None,
    "Erik - Estimate Accuracy Avg $": None,
    "Erik - Average Booked $ Amount": None,
    "Erik - Bad Lead % - by bad lead date received": None,
    "Erik - # of bundles of boxes per week": None,
    "Rebecca Total Booked $": None,
    "Rebecca - Valuation Sold $": None,
    "Rebecca - Booking %": None,
    "Rebecca - Estimate Accuracy Avg $": None,
    "Rebecca - Dials": None,
    "Rebecca - Talk Time": None,
    "Rebecca - 30% of Valuation Sales": None,
    "# of Valuation Closed": None
}

insights_page = smartmoving.insights

insights_page.open()

accounting_job_revenue_page = insights_page.accounting_job_revenue

accounting_job_revenue_page.open()

accounting_job_revenue_page.date_filter.click()
accounting_job_revenue_page.date_filter.select_value("Closed Date")

accounting_job_revenue_page.calendar_filter.click()
accounting_job_revenue_page.calendar_filter.select_value("This Week")

new_row["Accounting Job Revenue"] = accounting_job_revenue_page.get_net_revenue()
new_row["# of Valuation Closed"] = accounting_job_revenue_page.get_number_of_valuation_closed()
new_row["Valuation as % of Revenue"] = (
    accounting_job_revenue_page.get_total_valuation_cost()
    / new_row["Accounting Job Revenue"]
) * 100


accounting_job_revenue_page.close()

accounting_storage_revenue_page = insights_page.accounting_storage_revenue
accounting_storage_revenue_page.quick_date_filter.click()
accounting_storage_revenue_page.quick_date_filter.select_value("Current Week")
new_row["Accounting Storage Revenue"] = accounting_storage_revenue_page.get_net_invoiced()

new_row["Weekly Total Revenue"] = new_row["Accounting Job Revenue"] + new_row["Accounting Storage Revenue"]


accounting_storage_revenue_page.close()




booked_opportunities_by_date_booked_page = insights_page.booked_opportunities_by_date_booked
booked_opportunities_by_date_booked_page.open()

booked_opportunities_by_date_booked_page.calendar_filter.click()
booked_opportunities_by_date_booked_page.calendar_filter.select_value("This Week")

new_row["$ Booked Sales"] = booked_opportunities_by_date_booked_page.get_total_estimated_amount()

new_row["$ Booked PY"] = booked_opportunities_by_date_booked_page.get_total_estimated_amount_prior_year()

new_row["YoY Booking ($)"] = (new_row["$ Booked Sales"] - new_row["$ Booked PY"]) / new_row["$ Booked PY"]

booked_opportunities_by_date_booked_page.side_panel_filter.click()
booked_opportunities_by_date_booked_page.side_panel_filter.select_value("Sales Person", ["Erik Cairo"])
booked_opportunities_by_date_booked_page.side_panel_filter.apply()

new_row["Erik Total Booked $"] = booked_opportunities_by_date_booked_page.get_total_estimated_amount()
new_row["Erik # of Booked"] = booked_opportunities_by_date_booked_page.get_total_booked_count()

booked_opportunities_by_date_booked_page.side_panel_filter.click()
booked_opportunities_by_date_booked_page.side_panel_filter.select_value("Sales Person", ["Erik Cairo", "Rebecca Perez"])
booked_opportunities_by_date_booked_page.side_panel_filter.apply()

new_row["Rebecca Total Booked $"] = booked_opportunities_by_date_booked_page.get_total_estimated_amount()
new_row["Rebecca # of Booked"] = booked_opportunities_by_date_booked_page.get_total_booked_count()


booked_opportunities_by_date_booked_page.close()

booking_percent_by_service_date_page = insights_page.booking_percent_by_survey_type
booking_percent_by_service_date_page.open()
booking_percent_by_service_date_page.calendar_filter.click()
booking_percent_by_service_date_page.calendar_filter.select_value("This Week")
new_row["Erik Booking % On Site"] = booking_percent_by_service_date_page.get_on_site_survey_total_booked()
new_row["Erik Booking % No Survey"] = booking_percent_by_service_date_page.get_no_survey_total_booked_percentage()

booking_percent_by_service_date_page.close()


completed_moves_page = insights_page.completed_moves

completed_moves_page.open()
completed_moves_page.calendar_filter.click()
completed_moves_page.calendar_filter.select_value("This Week")

new_row["Completed Moves"] = completed_moves_page.get_total_moves()
new_row["Valuation on 30% of jobs"] = (new_row["# of Valuation Closed"] / new_row["Completed Moves"]) * 100

new_row["Average Ticket Amount"] = (new_row["Accounting Job Revenue"] / new_row["Completed Moves"]) * 100

completed_moves_page.close()


booked_opportunities_by_service_date_page = insights_page.booked_opportunities_by_service_date
booked_opportunities_by_service_date_page.open()
booked_opportunities_by_service_date_page.calendar_filter.click()
booked_opportunities_by_service_date_page.calendar_filter.select_value("Next Month")
new_row["Booked $ Next Month vs Forecast"] = booked_opportunities_by_service_date_page.get_total_estimated_amount()

booked_opportunities_by_service_date_page.close()

outstanding_balances_page = insights_page.outstanding_balances
outstanding_balances_page.open()
outstanding_balances_page.calendar_filter.click()
outstanding_balances_page.calendar_filter.select_value("This Year")

new_row["Aging A/R"] = outstanding_balances_page.get_total_balance()

outstanding_balances_page.close()

salesperson_performance_page = insights_page.salesperson_performance

salesperson_performance_page.date_type_filter.click()
salesperson_performance_page.date_type_filter.select_value("Lead Received Date")
salesperson_performance_page.calendar_filter.click()
salesperson_performance_page.calendar_filter.select_value("This Week")

new_row["Bad Leads %"] = salesperson_performance_page.get_bad_leads_percentage()

new_row["# Leads CY"] = salesperson_performance_page.get_bad_leads()
new_row["# Leads PY"] = salesperson_performance_page.get_total_bad_leads_prior_year()

new_row["YoY Net Lead Growth %"] = ((new_row["# Leads CY"] - new_row["# Leads PY"]) / new_row["# Leads Py"]) * 100
salesperson_performance_page.side_panel_filter.click()
salesperson_performance_page.side_panel_filter.select_value("Sales Person", ["Erik Cairo"])
salesperson_performance_page.side_panel_filter.apply()

new_row["Erik - Bad Lead % - by bad lead date received"] = salesperson_performance_page.get_bad_leads_percentage()


salesperson_performance_page.close()

lost_leads_and_opportunities_summary_page = insights_page.lost_leads_and_opportunities_summary
lost_leads_and_opportunities_summary_page.open()

lost_leads_and_opportunities_summary_page.date_filter.click()
lost_leads_and_opportunities_summary_page.date_filter.select_value("By Lost Date")

lost_leads_and_opportunities_summary_page.calendar_filter.click()
lost_leads_and_opportunities_summary_page.calendar_filter.select_value("This Week")

new_row["Lost leads & opportunities from pricing"] = lost_leads_and_opportunities_summary_page.get_price_too_high()

lost_leads_and_opportunities_summary_page.close()

estimate_accuracy_summary_page = insights_page.estimate_accuracy_summary
estimate_accuracy_summary_page.open()

estimate_accuracy_summary_page.calendar_filter.select_value("Last Week")

new_row["Erik - Estimate Accuracy Avg $"] = estimate_accuracy_summary_page.get_average_price()

estimate_accuracy_summary_page.close()

new_row["Erik - Average Booked $ Amount"] = new_row["Erik Total Booked $"] / new_row["Erik # of Booked"]

















