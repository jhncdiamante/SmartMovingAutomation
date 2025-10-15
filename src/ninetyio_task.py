from dotenv import load_dotenv
from src.Drivers.PlaywrightDriver.PlaywrightDriver import PlaywrightDriver
from src.Login.LoginCredentials import LoginCredentials

from src.CRM.Ninety.Pages.Scorecard import Scorecard
from src.CRM.Ninety.Pages.Tables.LeadershipTeam import LeaderShipTeam
from src.CRM.Ninety.Pages.Tables.SalesTeam import SalesTeam
from src.CRM.Ninety.Pages.Tables.SecondaryLeadership import SecondaryLeadership
from src.CRM.Ninety.Pages.Tables.CSRTeam import CSRTeam
from src.CRM.Ninety.Ninety import Ninety

import os
import time

# ---------------------------
# 1. Load environment variables
# ---------------------------
load_dotenv()
NINETY_USERNAME = os.getenv("NINETYIO_USERNAME")
NINETY_PASSWORD = os.getenv("NINETYIO_PASSWORD")

if not NINETY_USERNAME or not NINETY_PASSWORD:
    raise EnvironmentError("Missing NINETYIO_USERNAME or NINETYIO_PASSWORD in .env")

ninety_login_credentials = LoginCredentials(
    username=NINETY_USERNAME,
    password=NINETY_PASSWORD
)

# ---------------------------
# 2. Setup Playwright driver
# ---------------------------
driver = PlaywrightDriver(browser_type="chromium", headless=False)
driver.set_up_driver()
page = driver.page

# ---------------------------
# 3. Instantiate Page Objects
# ---------------------------
leadership_team_table = LeaderShipTeam(page)
sales_team = SalesTeam(page)
secondary_leadership = SecondaryLeadership(page)
csr_team = CSRTeam(page)

scorecard = Scorecard(
    page=page,
    leadership_team_table=leadership_team_table,
    sales_team=sales_team,
    csr_team=csr_team,
    secondary_leadership=secondary_leadership
)

ninety = Ninety(
    login_credentials=ninety_login_credentials,
    page=page,
    scorecard=scorecard
)

# ---------------------------
# 4. Login & interact with Scorecard
# ---------------------------
ninety.login()
ninety.scorecard.open()

time.sleep(5)
ninety.scorecard.sales_team.open()

time.sleep(5)
ninety.scorecard.sales_team.set_value(
    title="Erik - Total Booked $",
    value="82100",
    week="2025-10-13"
)
ninety.scorecard.leadership_team_table.open()

ninety.scorecard.leadership_team_table.set_value(
    title="Weekly Total Revenue",
    value="82100",
    week="2025-10-13"
)
ninety.scorecard.leadership_team_table.set_value(
    title="$ Booked Sales",
    value="123456",
    week="2025-10-13"
)
ninety.scorecard.leadership_team_table.set_value(
    title="Erik Booking % On Site",
    value="123456",
    week="2025-10-13"
)
ninety.scorecard.leadership_team_table.set_value(
    title="Booking % (No Survey Type)",
    value="123456",
    week="2025-10-13"
)
ninety.scorecard.leadership_team_table.set_value(
    title="Valuation on 30% of Jobs",
    value="123456",
    week="2025-10-13"
)
# ---------------------------
# 5. Keep session open for inspection
# ---------------------------
time.sleep(999999)  # Keep browser open
driver.close()
