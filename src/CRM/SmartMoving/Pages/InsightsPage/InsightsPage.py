
from src.CRM.Page import Page

class InsightsPage(Page):

    def close(self):
        self._logger.info("Closing Page...")
        self._driver.get("https://app.smartmoving.com/reports/smart-insights/lists")
        self._wait_for_complete_loading()