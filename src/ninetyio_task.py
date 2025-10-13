
from dotenv import load_dotenv

from src.Login.LoginCredentials import LoginCredentials
from src.SeleniumDriver.Driver import EdgeDriver
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

ninety_login_credentials = LoginCredentials(username=NINETY_USERNAME, password=NINETY_PASSWORD)

edge = EdgeDriver()
edge.set_up_driver()

sales_team = SalesTeam(edge.driver)
leadership_team_table = LeaderShipTeam(edge.driver)
secondary_leadership = SecondaryLeadership(edge.driver)
csr_team = CSRTeam(edge.driver)

scorecard = Scorecard(driver=edge.driver, leadership_team_table=leadership_team_table,
                sales_team=sales_team, secondary_leadership=secondary_leadership, csr_team=csr_team)


ninety = Ninety(login_credentials=ninety_login_credentials, selenium_driver=edge.driver, scorecard=scorecard)

ninety.login()
ninety.scorecard.open()
import time

time.sleep(5)
ninety.scorecard.leadership_team_table.open()
import time

time.sleep(5)
ninety.scorecard.leadership_team_table.set_value("Weekly Total Revenue", value="82100", week="2025-10-13")
ninety.scorecard.leadership_team_table.set_value("$ Booked Sales", value="12", week="2025-10-13")
ninety.scorecard.leadership_team_table.set_value("Erik Booking % On Site", value="34", week="2025-10-13")

import time
time.sleep(21312)

