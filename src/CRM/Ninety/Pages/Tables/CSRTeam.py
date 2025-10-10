
from src.CRM.Ninety.Pages.Tables.ScorecardTable import ScorecardTable
from undetected_chromedriver import By

class CSRTeam(ScorecardTable):

    @property
    def _locator(self):
        return By.XPATH, "//terra-option[.//text()[normalize-space()='CSR Team']]"

    
    
