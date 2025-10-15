
from src.CRM.Ninety.Pages.Tables.ScorecardTable import ScorecardTable

class SecondaryLeadership(ScorecardTable):

    @property
    def _locator(self):
        return "//terra-option[.//text()[normalize-space()='Secondary Leadership KPIs']]"

    def __str__(self) -> str:
        return "Secondary Leadership KPIs Table"

    
    
