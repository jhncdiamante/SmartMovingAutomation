from src.CRM.PlaywrightPage import PlaywrightPage
from src.CRM.Ninety.Pages.Tables.LeadershipTeam import LeaderShipTeam
from src.CRM.Ninety.Pages.Tables.SalesTeam import SalesTeam
from src.CRM.Ninety.Pages.Tables.SecondaryLeadership import SecondaryLeadership
from src.CRM.Ninety.Pages.Tables.CSRTeam import CSRTeam

class Scorecard(PlaywrightPage):
    def __init__(self, page, leadership_team_table: LeaderShipTeam, sales_team: SalesTeam, csr_team: CSRTeam, secondary_leadership: SecondaryLeadership):
        super().__init__(page)
        self.leadership_team_table = leadership_team_table
        self.sales_team = sales_team
        self.csr_team = csr_team
        self.secondary_leadership = secondary_leadership

    @property
    def _locator(self) -> str:
        return "//ninety-navigation-menu-item/button[.//text()[normalize-space()='Scorecard']]"
