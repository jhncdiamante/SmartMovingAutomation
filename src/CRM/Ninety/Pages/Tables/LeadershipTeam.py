
from src.CRM.Ninety.Pages.Tables.ScorecardTable import ScorecardTable

class LeaderShipTeam(ScorecardTable):

    @property
    def _locator(self):
        return "//terra-option[.//text()[normalize-space()='Leadership Team']]"

    def __str__(self) -> str:
        return "Leadership Team Table"

    
    
