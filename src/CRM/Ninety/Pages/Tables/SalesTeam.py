
from src.CRM.Ninety.Pages.Tables.ScorecardTable import ScorecardTable

class SalesTeam(ScorecardTable):

    @property
    def _locator(self) -> str:
        return "//terra-option[.//text()[normalize-space()='Sales Team']]"

    def __str__(self) -> str:
        return "Sales Team Table"

    
