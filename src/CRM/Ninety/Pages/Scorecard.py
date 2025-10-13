from src.CRM.Page import Page
from undetected_chromedriver import By
from src.CRM.Ninety.Pages.Tables.LeadershipTeam import LeaderShipTeam
from src.CRM.Ninety.Pages.Tables.SalesTeam import SalesTeam
from src.CRM.Ninety.Pages.Tables.SecondaryLeadership import SecondaryLeadership
from src.CRM.Ninety.Pages.Tables.CSRTeam import CSRTeam
from src.Chrome.IDriver import IDriver

class Scorecard(Page):
    def __init__(self, driver: IDriver, leadership_team_table: LeaderShipTeam,
    sales_team: SalesTeam, csr_team: CSRTeam, secondary_leadership: SecondaryLeadership):
        super().__init__(driver)
        self.leadership_team_table = leadership_team_table
        self.sales_team = sales_team
        self.csr_team = csr_team
        self.secondary_leadership = secondary_leadership
        
    @property
    def _locator(self) -> tuple[By, str]:
        return By.XPATH, "//ninety-navigation-menu-item/button[.//text()[normalize-space()='Scorecard']]"
