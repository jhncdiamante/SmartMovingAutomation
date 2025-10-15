
from src.CRM.Ninety.Pages.Tables.ScorecardTable import ScorecardTable

class CSRTeam(ScorecardTable):

    @property
    def _locator(self):
        return "//terra-option[.//text()[normalize-space()='CSR Team']]"

    def __str__(self) -> str:
        return "CSR Team Table"

    
    
