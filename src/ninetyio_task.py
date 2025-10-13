
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
import time
time.sleep(21312)

