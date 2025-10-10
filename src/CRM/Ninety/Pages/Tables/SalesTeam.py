
from src.CRM.Ninety.Pages.Tables.ScorecardTable import ScorecardTable
from undetected_chromedriver import By

class SalesTeam(ScorecardTable):

    @property
    def _locator(self):
        return By.XPATH, "//terra-option[.//text()[normalize-space()='Sales Team']]"

    
    
