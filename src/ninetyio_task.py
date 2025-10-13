
from dotenv import load_dotenv

from src.Login.LoginCredentials import LoginCredentials
from src.Chrome.Driver import ChromeDriver
from src.CRM.Ninety.Ninety import Ninety

from src.CRM.Ninety.Pages.Scorecard import Scorecard
from src.CRM.Ninety.Pages.Tables.LeadershipTeam import LeaderShipTeam
from src.CRM.Ninety.Pages.Tables.SalesTeam import SalesTeam
from src.CRM.Ninety.Pages.Tables.SecondaryLeadership import SecondaryLeadership
from src.CRM.Ninety.Pages.Tables.CSRTeam import CSRTeam
import os

load_dotenv()
NINETY_USERNAME = os.getenv("NINETYIO_USERNAME")
NINETY_PASSWORD = os.getenv("NINETYIO_PASSWORD")

metric_table = {
    "Leadership Team": [
        "Weekly Total Revenue",
        "$ Booked Sales",
        "Erik Booking % On Site",
        "Booking % (No Survey Type)",
        "Valuation on 30% of jobs",
        "Average Ticket Amount Completed Jobs",
        "Booked $ Next Month vs Forecast  (70% of Next Month Revenue Goal)",
        "Aging A/R",
        "YoY Net Lead Growth %"
    ],
    "Secondary Leadership KPIs": [
        "Completed Moves",
        "Valuation % of Revenue",
        "$ Booked PY",
        "YoY Booking ($)",
        "# Net Leads PY",
        "# Net Leads CY",
        "Bad Leads Received %",
        "Lost leads & opportunities from pricing",
        "# of movers",
        "# of drivers"
    ],
    "Sales Team": [
        "Erik - Total Booked $",
        "Erik - # Booked ",
        "Erik - # of Estimates",
        "Erik - Estimate Accuracy Avg $",
        "Erik - Average Booked $ Amount",
        "Erik - Bad Lead % - by bad lead date received",
        "Erik - # of bundles of boxes per week"
    ],
    "CSR Team": [
        "Rebecca - Booked $",
        "Rebecca - Valuation Sold $",
        "Rebecca - Booking %",
        "Rebecca - Estimate Accuracy Avg $",
        "Rebecca - Dials",
        "Rebecca - Talk Time"
    ],
    "EON": [
        "Accounting Job Revenue",
        "Accounting Storage Revenue",
        "Rebecca - 30% of Valuation Sales",
        "# of Valuation Closed"
    ]
}


ninety_login_credentials = LoginCredentials(username=NINETY_USERNAME, password=NINETY_PASSWORD)

chrome = ChromeDriver()
chrome.set_up_driver()

sales_team = SalesTeam(chrome.driver)
leadership_team_table = LeaderShipTeam(chrome.driver)
secondary_leadership = SecondaryLeadership(chrome.driver)
csr_team = CSRTeam(chrome.driver)

scorecard = Scorecard(driver=chrome.driver, leadership_team_table=leadership_team_table,
                sales_team=sales_team, secondary_leadership=secondary_leadership, csr_team=csr_team)


ninety = Ninety(login_credentials=ninety_login_credentials, selenium_driver=chrome.driver, scorecard=scorecard)

ninety.login()
ninety.scorecard.open()

ninety.scorecard.leadership_team_table.open()
ninety.scorecard.leadership_team_table.set_value("Weekly Total Revenue", value="82100", week="2025-10-13")
for metric in metric_table["Leadership Team"]:
    ninety.scorecard.leadership_team_table.set_value(metric, value=new_row[metric], week=start_of_week)



import time
time.sleep(21312)

