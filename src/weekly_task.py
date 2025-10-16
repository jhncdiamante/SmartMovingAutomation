import os
import time
from datetime import date, timedelta
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

from selenium.webdriver.support.ui import WebDriverWait

from src.CRM.SmartMoving.Filters.QuickDateFilter import QuickDateFilter
from src.CRM.SmartMoving.Filters.SalespersonPerformanceDateTypeFilter import SalespersonPerformanceDateTypeFilter
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from src.CRM.SmartMoving.Pages.InsightsPage.CompletedMoves import CompletedMoves
from src.Login.LoginCredentials import LoginCredentials
from src.Drivers.SeleniumDriver.Driver import ChromeDriver
from src.CRM.SmartMoving.SmartMoving import SmartMoving
from src.CRM.SmartMoving.Pages.Calendars import Calendars
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter, OfficeCalendarUserFilter
from src.CRM.SmartMoving.Pages.Sales import Sales
from src.CRM.SmartMoving.Filters.SalesDashboardFilter import SalesDashboardSalesPersonFilter
from src.CRM.SmartMoving.Pages.Settings import Settings
from src.CRM.SmartMoving.Pages.InsightsPage.BookOpportunitiesByDateBooked import BookedOpportunitiesByDateBooked

from src.CRM.SmartMoving.Pages.Insights import Insights
from src.CRM.SmartMoving.Pages.InsightsPage.AccountingJobRevenue import AccountingJobRevenue
from src.CRM.SmartMoving.Filters.AccountingJobRevenueDateTypeFilter import AccountingJobRevenueDateFilter
from src.CRM.SmartMoving.Filters.SidePanelFilter import SidePanelFilter
from src.CRM.SmartMoving.Pages.InsightsPage.BookOpportunitiesByServiceDate import BookedOpportunitiesByServiceDate

from src.CRM.SmartMoving.Pages.InsightsPage.AccountingStorageRevenue import AccountingStorageRevenue
from src.CRM.SmartMoving.Pages.InsightsPage.BookingPercentBySurveyType import BookingPercentBySurveyType
from src.CRM.SmartMoving.Pages.InsightsPage.EstimateAccuracySummary import EstimateAccuracySummary
from src.CRM.SmartMoving.Pages.InsightsPage.LostLeadsAndOpportunitiesSummary import LostLeadsAndOpportunitiesSummary
from src.CRM.SmartMoving.Pages.InsightsPage.OutstandingBalances import OutstandingBalances
from src.CRM.SmartMoving.Pages.InsightsPage.SalespersonPerformance import SalespersonPerformance
from src.CRM.SmartMoving.Filters.LostLeadsAndOpportunitiesSummaryDateFilter import LostLeadsAndOpportunitiesSummaryDateFilter

from src.Helpers.logging_config import setup_logger
logging = setup_logger(__name__)

from src.CRM.Ninety.Ninety import Ninety
from src.CRM.Ninety.Pages.Scorecard import Scorecard
from src.CRM.Ninety.Pages.Tables.LeadershipTeam import LeaderShipTeam
from src.CRM.Ninety.Pages.Tables.SalesTeam import SalesTeam
from src.CRM.Ninety.Pages.Tables.SecondaryLeadership import SecondaryLeadership
from src.CRM.Ninety.Pages.Tables.CSRTeam import CSRTeam


# ---------- helpers ----------
def safe_div(a, b, default=0.0):
    try:
        if a is None or b in (None, 0):
            return default
        return a / b
    except Exception:
        return default



# ---------- env & login ----------
load_dotenv()
SMARTMOVING_USERNAME = os.getenv("SMARTMOVING_USERNAME")
SMARTMOVING_PASSWORD = os.getenv("SMARTMOVING_PASSWORD")
NINETY_USERNAME = os.getenv("NINETYIO_USERNAME")
NINETY_PASSWORD = os.getenv("NINETYIO_PASSWORD")

smartmoving_login_credentials = LoginCredentials(username=SMARTMOVING_USERNAME, password=SMARTMOVING_PASSWORD)

chrome = ChromeDriver()
chrome.set_up_driver()
driver = chrome.driver

# page objects & filters
office_calendar_event_filter = OfficeCalendarEventFilter(driver=driver)
office_calendar_user_filter = OfficeCalendarUserFilter(driver=driver)
calendars_page = Calendars(
    route="https://app.smartmoving.com/calendars/office",
    driver=driver,
    office_calendar_event_dropdown_filter=office_calendar_event_filter,
    office_calendar_user_dropdown_filter=office_calendar_user_filter
)
sales_filter = SalesDashboardSalesPersonFilter(driver=driver)
sales_page = Sales(route="https://app.smartmoving.com/sales/dashboard", driver=driver, sales_dropdown_filter=sales_filter)
settings_page = Settings(route="https://app.smartmoving.com/settings", driver=driver)
accounting_job_revenue_date_filter = AccountingJobRevenueDateFilter(driver=driver)
calendar_filter = CalendarFilter(driver=driver)
side_panel_filter = SidePanelFilter(driver=driver)
quick_date_filter = QuickDateFilter(driver=driver)
salesperson_performance_date_type_filter = SalespersonPerformanceDateTypeFilter(driver=driver)
lost_leads_and_opp_date_type_filter = LostLeadsAndOpportunitiesSummaryDateFilter(driver=driver)

insights_page = Insights(
    route="https://app.smartmoving.com/reports/smart-insights/lists",
    driver=driver,
    accounting_job_revenue=AccountingJobRevenue(driver=driver, date_filter=accounting_job_revenue_date_filter, calendar_filter=calendar_filter),
    booked_opportunities_by_date_booked=BookedOpportunitiesByDateBooked(driver=driver, calendar_filter=calendar_filter, side_panel_filter=side_panel_filter),
    booking_percent_by_survey_type=BookingPercentBySurveyType(driver=driver, calendar_filter=calendar_filter),
    accounting_storage_revenue=AccountingStorageRevenue(driver=driver, quick_date_filter=quick_date_filter),
    booked_opportunities_by_service_date=BookedOpportunitiesByServiceDate(driver=driver, calendar_filter=calendar_filter, side_panel_filter=side_panel_filter),
    outstanding_balances=OutstandingBalances(driver=driver, calendar_filter=calendar_filter),
    salesperson_performance=SalespersonPerformance(driver=driver, calendar_filter=calendar_filter, date_type_filter=salesperson_performance_date_type_filter, side_panel_filter=side_panel_filter),
    lost_leads_and_opportunities_summary=LostLeadsAndOpportunitiesSummary(driver=driver, calendar_filter=calendar_filter, date_filter=lost_leads_and_opp_date_type_filter),
    estimate_accuracy_summary=EstimateAccuracySummary(driver=driver, calendar_filter=calendar_filter),
    completed_moves=CompletedMoves(driver=driver, calendar_filter=calendar_filter)
)

smartmoving = SmartMoving(
    login_credentials=smartmoving_login_credentials,
    selenium_driver=driver,
    calendars_page=calendars_page,
    sales_page=sales_page,
    settings_page=settings_page,
    insights_page=insights_page
)

# login
smartmoving.login()
WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

today = date.today()
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)
date_str = f"{start_of_week} to {end_of_week}"

# canonical new_row keys — normalized and exact
new_row = {col: None for col in [
    "Date", "Weekly Total Revenue", "Accounting Job Revenue", "Accounting Storage Revenue", "$ Booked Sales",
    "YoY Net Lead Growth", "Erik Booking % On Site", "Booking % (No Survey Type)", "Valuation on 30% of Jobs",
    "Average Ticket Amount Completed Jobs", "Booked $ Next Month vs Forecast  (70% of Next Month Revenue Goal)",
    "Aging A/R", "Completed Moves", "Valuation % of Revenue", "$ Booked PY", "YoY Booking Growth $", "# Net Leads PY",
    "# Net Leads CY", "Bad Leads Received %", "Lost Leads & Opportunities from Pricing", "# of Movers", "# of Drivers",
    "Erik - Total Booked $", "Erik - # Booked", "Erik - # of Estimates", "Erik - Estimate Accuracy Avg $",
    "Erik - Average Booked $ Amount", "Erik - Bad Lead % - by bad lead date received",
    "Erik - # of bundles of boxes per week", "Rebecca - Booked $", "Rebecca - Valuation Sold $",
    "Rebecca - Booking %", "Rebecca - Estimate Accuracy", "Rebecca - Dials", "Rebecca - Talk Time",
]}


new_row["Date"] = date_str

insights_page = smartmoving.insights
insights_page.open()

# ---------- ACCOUNTING JOB REVENUE ----------
page = insights_page.accounting_job_revenue
page.open()
page.date_filter.click()
page.date_filter.select_value("Closed Date")
page.calendar_filter.click()
page.calendar_filter.select_value("This Week")

page.open_modal("Valuation")
num_of_valuation_closed = page.get_number_of_valuation_closed()
total_valuation_cost = page.get_total_valuation_cost()
page.close_modal()

new_row["Accounting Job Revenue"] = page.get_net_revenue()
new_row["Valuation % of Revenue"] = safe_div(total_valuation_cost, new_row["Accounting Job Revenue"])
page.close()

# ---------- ACCOUNTING STORAGE REVENUE ----------
page = insights_page.accounting_storage_revenue
page.open()
page.quick_date_filter.click()
page.quick_date_filter.select_value("Current Week")
new_row["Accounting Storage Revenue"] = page.get_net_invoiced()
new_row["Weekly Total Revenue"] = (new_row["Accounting Job Revenue"] or 0) + (new_row["Accounting Storage Revenue"] or 0)
page.close()

# ---------- BOOKED OPPORTUNITIES BY DATE BOOKED ----------
page = insights_page.booked_opportunities_by_date_booked
new_row["$ Booked PY"] = page.get_total_estimated_amount_prior_year()
page.open()
page.calendar_filter.click()
page.calendar_filter.select_value("This Week")
new_row["$ Booked Sales"] = page.get_total_estimated_amount()
new_row["YoY Booking Growth $"] = safe_div(
    (new_row["$ Booked Sales"] or 0) - (new_row["$ Booked PY"] or 0),
    (new_row["$ Booked PY"] or 0)
)
page.side_panel_filter.click()
page.side_panel_filter.select_value("Sales Person", ["Erik Cairo"])
page.side_panel_filter.apply()
page.side_panel_filter.close()
new_row["Erik - Total Booked $"] = page.get_total_estimated_amount()
new_row["Erik - # Booked"] = page.get_total_booked_count()
page.side_panel_filter.click()
page.side_panel_filter.select_value("Sales Person", ["Erik Cairo", "Rebecca Perez"])
page.side_panel_filter.apply()
page.side_panel_filter.close()
new_row["Rebecca - Booked $"] = page.get_total_estimated_amount()
page.close()

# ---------- BOOKING PERCENT BY SURVEY TYPE ----------
page = insights_page.booking_percent_by_survey_type
page.open()
page.calendar_filter.click()
page.calendar_filter.select_value("This Week")
new_row["Erik Booking % On Site"] = page.get_on_site_survey_total_booked_percentage()
new_row["Booking % (No Survey Type)"] = page.get_no_survey_total_booked_percentage()
page.close()

# ---------- COMPLETED MOVES ----------
page = insights_page.completed_moves
page.open()
page.calendar_filter.click()
page.calendar_filter.select_value("This Week")
new_row["Completed Moves"] = page.get_total_moves()
new_row["Valuation on 30% of Jobs"] = safe_div(num_of_valuation_closed, new_row["Completed Moves"])
new_row["Average Ticket Amount Completed Jobs"] = safe_div(new_row["Accounting Job Revenue"], new_row["Completed Moves"])
page.close()

# ---------- BOOKED OPP BY SERVICE DATE ----------
page = insights_page.booked_opportunities_by_service_date
page.open()
page.calendar_filter.click()
page.calendar_filter.select_value("Next Month")
new_row["Booked $ Next Month vs Forecast  (70% of Next Month Revenue Goal)"] = page.get_total_estimated_amount()
page.close()

# ---------- OUTSTANDING BALANCES ----------
page = insights_page.outstanding_balances
page.open()
page.calendar_filter.click()
page.calendar_filter.select_value("This Year")
new_row["Aging A/R"] = page.get_total_balance()
page.close()

# ---------- SALESPERSON PERFORMANCE ----------
page = insights_page.salesperson_performance
page.open()
new_row["# Net Leads PY"] = page.get_total_leads_received_prior_year()
page.date_type_filter.click()
page.date_type_filter.select_value("Lead Received Date")
page.calendar_filter.click()
page.calendar_filter.select_value("This Week")

total_bad_leads = page.get_bad_leads()
leads_received = page.get_leads_received()

new_row["Bad Leads Received %"] = safe_div(total_bad_leads, leads_received) * 100
new_row["# Net Leads CY"] = (leads_received or 0) - (total_bad_leads or 0)
new_row["YoY Net Lead Growth"] = safe_div(
    new_row["# Net Leads CY"] - new_row["# Net Leads PY"],
    new_row["# Net Leads PY"]
)

page.side_panel_filter.click()
page.side_panel_filter.select_value("Sales Person", ["Erik Cairo"])
page.side_panel_filter.apply()
page.side_panel_filter.close()
new_row["Erik - Bad Lead % - by bad lead date received"] = safe_div(page.get_bad_leads(), page.get_leads_received())

page.side_panel_filter.click()
page.side_panel_filter.select_value("Sales Person", ["Erik Cairo", "Rebecca Perez"])
page.side_panel_filter.apply()
page.side_panel_filter.close()
new_row["Rebecca - Booking %"] = safe_div(new_row["Rebecca - Booked $"], leads_received - total_bad_leads)
page.close()

# ---------- LOST LEADS & OPP SUMMARY ----------
page = insights_page.lost_leads_and_opportunities_summary
page.open()
page.date_filter.click()
page.date_filter.select_value("By Lost Date")
page.calendar_filter.click()
page.calendar_filter.select_value("This Week")
new_row["Lost Leads & Opportunities from Pricing"] = page.get_price_too_high()
page.close()

# ---------- ESTIMATE ACCURACY SUMMARY ----------
page = insights_page.estimate_accuracy_summary
page.open()
page.calendar_filter.click()
page.calendar_filter.select_value("Last Week")
new_row["Erik - Estimate Accuracy Avg $"] = page.get_average_price("Erik Cairo")
new_row["Rebecca - Estimate Accuracy"] = page.get_average_price("Rebecca Perez")
page.close()

new_row["Erik - Average Booked $ Amount"] = safe_div(
    new_row["Erik - Total Booked $"],
    new_row["Erik - # Booked"]
)

# ---------- SETTINGS: crew members ----------
settings_page = smartmoving.settings
settings_page.open()
crew_members = settings_page.get_all_crew_members()
new_row["# of Movers"] = len([n for n in crew_members if "(" not in n])
new_row["# of Drivers"] = len([n for n in crew_members if "(D)" in n])

# ---------- GOOGLE SHEETS ----------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Copy of Daily KPIs - MasterMovers")

# appointments
calendar_ws = sheet.worksheet("appointments")
existing = calendar_ws.get_all_values()
if existing and len(existing) > 1:
    cols = existing[0]
    df = pd.DataFrame(existing[1:], columns=cols)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["# of Apt"] = pd.to_numeric(df["# of Apt"], errors="coerce").fillna(0)
    start, end = pd.Timestamp(start_of_week), pd.Timestamp(end_of_week)
    wdf = df[(df["Date"] >= start) & (df["Date"] <= end)]
    new_row["Erik - # of Estimates"] = int(wdf["# of Apt"].sum(skipna=True))


# boxes
calendar_ws = sheet.worksheet("boxes")
existing = calendar_ws.get_all_values()
if existing and len(existing) > 1:
    cols = existing[0]
    df = pd.DataFrame(existing[1:], columns=cols)
    df.dropna(subset=['Drop-Off Date', 'No. of Bundles'], inplace=True)
    df["Drop-Off Date"] = pd.to_datetime(df["Drop-Off Date"], errors="coerce")
    df["No. of Bundles"] = pd.to_numeric(df["No. of Bundles"], errors="coerce").fillna(0)
    start, end = pd.Timestamp(start_of_week), pd.Timestamp(end_of_week)
    wdf = df[(df["Drop-Off Date"] >= start) & (df["Drop-Off Date"] <= end)]
    new_row["Erik - # of bundles of boxes per week"] = int(wdf["No. of Bundles"].sum(skipna=True))


# val-sold
val_ws = sheet.worksheet("val-sold")
existing = val_ws.get_all_values()
if existing and len(existing) > 1:
    cols = existing[0]
    df = pd.DataFrame(existing[1:], columns=cols)
    df = df[df["SALES REP NAME"].astype(str).str.contains("Rebecca", case=False)]
    df["DATE SOLD (RONEL)"] = pd.to_datetime(df["DATE SOLD (RONEL)"], errors="coerce")
    df = df[(df["DATE SOLD (RONEL)"] >= start) & (df["DATE SOLD (RONEL)"] <= end)]
    df["VALUATION AMOUNT"] = (
        df["VALUATION AMOUNT"].astype(str)
        .str.replace("$", "")
        .str.replace(",", "")
        .astype(float)
    )
    new_row["Rebecca - Valuation Sold $"] = df["VALUATION AMOUNT"].sum()

# dialpad
dial_ws = sheet.worksheet("dialpad")
existing = dial_ws.get_all_values()
if existing and len(existing) > 1:
    cols = existing[0]
    df = pd.DataFrame(existing[1:], columns=cols)
    df = df[df["name"].astype(str).str.contains("Rebecca Perez", case=False)]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[(df["date"] >= start) & (df["date"] <= end)]
    new_row["Rebecca - Dials"] = df["outbound_calls"].astype(float).sum()
    new_row["Rebecca - Talk Time"] = df["talk_duration"].astype(float).sum()

weekly_kpis = sheet.worksheet("Weekly KPI")


logging.info(f"Appending new row: {new_row}")

weekly_kpis.append_row([new_row[key] for key in new_row.keys()])      


# ---------- TRANSFER TO NINETY.IO ----------
metric_table = {
    "Leadership Team": [
        "Weekly Total Revenue",
        "$ Booked Sales",
        "YoY Net Lead Growth",
        "Erik Booking % On Site",
        "Booking % (No Survey Type)",
        "Valuation on 30% of Jobs",
        "Average Ticket Amount Completed Jobs",
        "Booked $ Next Month vs Forecast  (70% of Next Month Revenue Goal)",
        "Aging A/R",
    ],
    "Secondary Leadership KPIs": [
        "Completed Moves",
        "Valuation % of Revenue",
        "$ Booked PY",
        "YoY Booking Growth $",
        "# Net Leads PY",
        "# Net Leads CY",
        "Bad Leads Received %",
        "Lost Leads & Opportunities from Pricing",
        "# of Movers",
        "# of Drivers",
    ],
    "Sales Team": [
        "Erik - Total Booked $",
        "Erik - # Booked",
        "Erik - # of Estimates",
        "Erik - Estimate Accuracy Avg $",
        "Erik - Average Booked $ Amount",
        "Erik - Bad Lead % - by bad lead date received",
        "Erik - # of bundles of boxes per week",
    ],
    "CSR Team": [
        "Rebecca - Booked $",
        "Rebecca - Valuation Sold $",
        "Rebecca - Booking %",
        "Rebecca - Estimate Accuracy",
        "Rebecca - Dials",
        "Rebecca - Talk Time",
    ],
}


# ---------- cleanup ----------
try:
    driver.quit()
except Exception as e:
    logging.warning(f"Error quitting driver: {e}")

from src.CRM.Ninety.Ninety import Ninety
from src.Drivers.PlaywrightDriver.PlaywrightDriver import PlaywrightDriver

driver = PlaywrightDriver(browser_type="chromium", headless=False)
driver.set_up_driver()
page = driver.page

ninety_login_credentials = LoginCredentials(username=NINETY_USERNAME, password=NINETY_PASSWORD)
sales_team = SalesTeam(page=page)
leadership_team_table = LeaderShipTeam(page=page)
secondary_leadership = SecondaryLeadership(page=page)
csr_team = CSRTeam(page=page)

scorecard = Scorecard(page=page, leadership_team_table=leadership_team_table,
                      sales_team=sales_team, secondary_leadership=secondary_leadership, csr_team=csr_team)

ninety = Ninety(login_credentials=ninety_login_credentials, page=page, scorecard=scorecard)
ninety.login()
ninety.scorecard.open()

table_map = {
    "Leadership Team": ninety.scorecard.leadership_team_table,
    "Secondary Leadership KPIs": ninety.scorecard.secondary_leadership,
    "Sales Team": ninety.scorecard.sales_team,
    "CSR Team": ninety.scorecard.csr_team,
}


for table_name, metrics in metric_table.items():
    table = table_map.get(table_name)
    if table is None:
        logging.error(f"No Ninety table mapped for {table_name}, skipping.")
        continue
    table.open()

    for metric in metrics:
        value = new_row.get(metric)
        # send value (table.set_value is assumed to handle locating and sending keys)
        table.set_value(metric, value=value, week=str(start_of_week))
        # small wait for the value propagation
        time.sleep(2)

