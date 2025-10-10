
from src.CRM.Ninety.Pages.Tables.ScorecardTable import ScorecardTable
from undetected_chromedriver import By

class SecondaryLeadership(ScorecardTable):

    @property
    def _locator(self):
        return By.XPATH, "//terra-option[.//text()[normalize-space()='Secondary Leadership KPIs']]"

    
    
